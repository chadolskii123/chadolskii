from .base import *

from .production import *

# 로컬이 프로덕션에서 사용되지 않게 하기 위한 방식
# Debug가 False로 되어있어야만 프로덕션에서 사용 할 수 있기 때문에
# 실제 운영 서버에서는 local셋팅이 import되지 않음
from .local import *

try:
    from .local import *
except:
    pass
