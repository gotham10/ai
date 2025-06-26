local u = "hi"
local j = game:GetService("HttpService")
local r = request({
    Url = "https://ai-zs6m.onrender.com",
    Method = "POST",
    Headers = {
        ["Content-Type"] = "application/json"
    },
    Body = j:JSONEncode({prompt = u})
})
print(j:JSONDecode(r.Body).response)
