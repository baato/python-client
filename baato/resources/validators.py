import re
import inspect
import itertools
from collections import OrderedDict

from decorator import decorator


class ValidationFailure(Exception):
    def __init__(self, func, args):
        self.func = func
        self.__dict__.update(args)

    def __repr__(self):
        return "ValidationFailure(func={func}, args={args})".format(
            func=self.func.__name__, args=dict([(k, v) for (k, v) in self.__dict__.items() if k != "func"])
        )

    def __str__(self):
        return repr(self)

    def __unicode__(self):
        return repr(self)

    def __bool__(self):
        return False

    def __nonzero__(self):
        return False


def func_args_as_dict(func, args, kwargs):
    """
    Return given function's positional and key value arguments as an ordered
    dictionary.
    """
    _getargspec = inspect.getfullargspec

    arg_names = list(OrderedDict.fromkeys(itertools.chain(_getargspec(func)[0], kwargs.keys())))
    return OrderedDict(list(zip(arg_names, args)) + list(kwargs.items()))


def validator(func, *args, **kwargs):
    """
    A decorator that makes given function validator.
    Whenever the given function is called and returns ``False`` value
    this decorator returns :class:`ValidationFailure` object.
    Example::
        >>> @validator
        ... def even(value):
        ...     return not (value % 2)
        >>> even(4)
        True
        >>> even(5)
        ValidationFailure(func=even, args={'value': 5})
    :param func: function to decorate
    :param args: positional function arguments
    :param kwargs: key value function arguments
    """

    def wrapper(func, *args, **kwargs):
        value = func(*args, **kwargs)
        if not value:
            return ValidationFailure(func, func_args_as_dict(func, args, kwargs))
        return True

    return decorator(wrapper, func)


ip_middle_octet = r"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5]))"
ip_last_octet = r"(?:\.(?:0|[1-9]\d?|1\d\d|2[0-4]\d|25[0-5]))"

regex = re.compile(  # noqa: W605
    r"^"
    # protocol identifier
    r"(?:(?:https?|ftp)://)"
    # user:pass authentication
    r"(?:[-a-z\u00a1-\uffff0-9._~%!$&'()*+,;=:]+" r"(?::[-a-z0-9._~%!$&'()*+,;=:]*)?@)?" r"(?:" r"(?P<private_ip>"
    # IP address exclusion
    # private & local networks
    r"(?:(?:10|127)" + ip_middle_octet + r"{2}" + ip_last_octet + r")|"
    r"(?:(?:169\.254|192\.168)" + ip_middle_octet + ip_last_octet + r")|"
    r"(?:172\.(?:1[6-9]|2\d|3[0-1])" + ip_middle_octet + ip_last_octet + r"))"
    r"|"
    # private & local hosts
    r"(?P<private_host>" r"(?:localhost))" r"|"
    # IP address dotted notation octets
    # excludes loopback network 0.0.0.0
    # excludes reserved space >= 224.0.0.0
    # excludes network & broadcast addresses
    # (first & last IP address of each class)
    r"(?P<public_ip>" r"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])" r"" + ip_middle_octet + r"{2}" r"" + ip_last_octet + r")" r"|"
    # IPv6 RegEx from https://stackoverflow.com/a/17871737
    r"\[("
    # 1:2:3:4:5:6:7:8
    r"([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|"
    # 1::                              1:2:3:4:5:6:7::
    r"([0-9a-fA-F]{1,4}:){1,7}:|"
    # 1::8             1:2:3:4:5:6::8  1:2:3:4:5:6::8
    r"([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|"
    # 1::7:8           1:2:3:4:5::7:8  1:2:3:4:5::8
    r"([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|"
    # 1::6:7:8         1:2:3:4::6:7:8  1:2:3:4::8
    r"([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|"
    # 1::5:6:7:8       1:2:3::5:6:7:8  1:2:3::8
    r"([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|"
    # 1::4:5:6:7:8     1:2::4:5:6:7:8  1:2::8
    r"([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|"
    # 1::3:4:5:6:7:8   1::3:4:5:6:7:8  1::8
    r"[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|"
    # ::2:3:4:5:6:7:8  ::2:3:4:5:6:7:8 ::8       ::
    r":((:[0-9a-fA-F]{1,4}){1,7}|:)|"
    # fe80::7:8%eth0   fe80::7:8%1
    # (link-local IPv6 addresses with zone index)
    r"fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|"
    r"::(ffff(:0{1,4}){0,1}:){0,1}"
    r"((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}"
    # ::255.255.255.255   ::ffff:255.255.255.255  ::ffff:0:255.255.255.255
    # (IPv4-mapped IPv6 addresses and IPv4-translated addresses)
    r"(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|"
    r"([0-9a-fA-F]{1,4}:){1,4}:"
    r"((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}"
    # 2001:db8:3:4::192.0.2.33  64:ff9b::192.0.2.33
    # (IPv4-Embedded IPv6 Address)
    r"(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])" r")\]|"
    # host name
    r"(?:(?:(?:xn--[-]{0,2})|[a-z\u00a1-\uffff\U00010000-\U0010ffff0-9]-?)*" r"[a-z\u00a1-\uffff\U00010000-\U0010ffff0-9]+)"
    # domain name
    r"(?:\.(?:(?:xn--[-]{0,2})|[a-z\u00a1-\uffff\U00010000-\U0010ffff0-9]-?)*"
    r"[a-z\u00a1-\uffff\U00010000-\U0010ffff0-9]+)*"
    # TLD identifier
    r"(?:\.(?:(?:xn--[-]{0,2}[a-z\u00a1-\uffff\U00010000-\U0010ffff0-9]{2,})|"
    r"[a-z\u00a1-\uffff\U00010000-\U0010ffff]{2,}))"
    r")"
    # port number
    r"(?::\d{2,5})?"
    # resource path
    r"(?:/[-a-z\u00a1-\uffff\U00010000-\U0010ffff0-9._~%!$&'()*+,;=:@/]*)?"
    # query string
    r"(?:\?\S*)?"
    # fragment
    r"(?:#\S*)?" r"$",
    re.UNICODE | re.IGNORECASE,
)

pattern = re.compile(regex)


@validator
def url_validator(value, public=False):
    """
    Return whether or not given value is a valid URL.
    If the value is valid URL this function returns ``True``, otherwise
    :class:`~validators.utils.ValidationFailure`.
    This validator is based on the wonderful `URL validator of dperini`_.
    .. _URL validator of dperini:
        https://gist.github.com/dperini/729294
    Examples::
        >>> url('http://foobar.dk')
        True
        >>> url('ftp://foobar.dk')
        True
        >>> url('http://10.0.0.1')
        True
        >>> url('http://foobar.d')
        ValidationFailure(func=url, ...)
        >>> url('http://10.0.0.1', public=True)
        ValidationFailure(func=url, ...)
    .. versionadded:: 0.2
    .. versionchanged:: 0.10.2
        Added support for various exotic URLs and fixed various false
        positives.
    .. versionchanged:: 0.10.3
        Added ``public`` parameter.
    .. versionchanged:: 0.11.0
        Made the regular expression this function uses case insensitive.
    .. versionchanged:: 0.11.3
        Added support for URLs containing localhost
    :param value: URL address string to validate
    :param public: (default=False) Set True to only allow a public IP address
    """
    result = pattern.match(value)
    if not public:
        return result

    return result and not any((result.groupdict().get(key) for key in ("private_ip", "private_host")))
