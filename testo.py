import jwt
import datetime

playload = {
    "exp": datetime.datetime.now() + datetime.timedelta(days=1, seconds=5),
    "iat": datetime.datetime.now(),
    "sub": 1
}
code = jwt.encode(
    playload,
    "super-key",
    algorithm="HS256"
)
print(code)
playload2 = jwt.decode("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTU4NDEwNDUsImlhdCI6MTYxNTc1NDY0MCwic3ViIjozfQ.VgPEi3ywnGBtkxFDgITl3sp5_oTAoA_3zIuWJbmwElY", "super-key",algorithms="HS256")
print(playload2)