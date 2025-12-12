import sys
import pytest
print('Running pytest via Python API...')
exit_code = pytest.main(['-q'])
print('pytest exit code:', exit_code)
sys.exit(exit_code)
