import redis
r = redis.Redis()
r.mset({"Croatia": "Zagreb", "Bahamas": "Nassau"})
r.sadd
print(r.get("Bahamas"))

r.set("test-key", "test-val")
print(r.get("test-key"))

dic = {
    "name": "Sidharrth",
    "age": "18"
}

r.hset("testdict", None, None, dic)

print(r.hgetall('testdict')[b'name'])

r.lpush('articles', 'This is article 1')
print(r.lrange('articles', 0, -1))