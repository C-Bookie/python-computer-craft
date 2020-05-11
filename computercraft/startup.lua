local file_path = 'back.lua'
local url = 'http://127.0.0.1:8080/'

print("Updating "..file_path)

if (fs.exists(file_path)) then
    fs.delete(file_path)
end

local function attempt_get(url)
    print(url)
    local r = http.get(url, nil)
    if (r == nil) then
        print("Response nil")
        return false
    else
        local response = r.getResponseCode()
        if (response ~= 200) then
            print('Response '..response)
            return false
        end
    end
    return r
end

local response = attempt_get(url..file_path, "")
local content = response.readAll()

local file = fs.open(file_path, "wb")
file.write(content)
file.close()

print("Running "..file_path)

os.run({}, file_path)

