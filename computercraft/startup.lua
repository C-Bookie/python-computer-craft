local file_path = 'back.lua'
local url = 'http://127.0.0.1:8080/'

local function attempt_get(url)
    write(url)
    local response = http.get(url, nil)
    if (response == nil) then
        print(" - nil")
    else
        local code = response.getResponseCode()
        print(' - '..code)
        if (code ~= 200) then
            return nil
        end
    end
    return response
end

print("Downloading "..file_path)
local response = attempt_get(url..file_path, "")

if (response ~= nil) then
    print("Updating "..file_path)
    local content = response.readAll()

    if (fs.exists(file_path)) then
        fs.delete(file_path)
    end

    local file = fs.open(file_path, "wb")
    file.write(content)
    file.close()
end
print("Running "..file_path)

os.run({}, file_path)

