local back = peripheral.wrap("top")
local monitors = {
    "monitor_0",
    "monitor_1",
}

local rules = {}
local sizes = {}

sizes["monitor_0"] = 1
rules["monitor_0"] = {
    "                                 RULES:",
    "",
    "1. No hacks exploits or third-party cheat systems.",
    "",
    "2. No overly offensive or racist language.",
    "",
    "3. Though historical buildings are not enforced they are appreciated.",
    "",
    "4. No aggressive world griefing outside of world wars",
    "",
    "5. No attempting to destroy dismantle or damage spawn island.",
    "",
    "6. No bypassing protection or land claims with exploits."
}

sizes["monitor_1"] = 1
rules["monitor_1"] = {
    "                                 TIPS:",
    "",
    "To found a country, use:",
    "  /f c [country tag] [country name]",
    "",
    "To see the world map, use:",
    "  /geotool",
    "",
    "To claim faction land use:",
    "  /f claim",
    "",
    "To set faction home, use",
    "  /f sethome",
    "",
    "To claim land using map gui, use:",
    "  /f map",
    "",
    "To invite someone to you're faction, use",
    "  /f invite"
}


for i in pairs(monitors) do
    local monitor = monitors[i]
    back.callRemote(monitor, "clear")
    back.callRemote(monitor, "setTextScale", sizes[monitor])
    for i in pairs(rules[monitor]) do
        local rule = rules[monitor][i]
        print(rule)
        back.callRemote(monitor, "setCursorPos", 1, i)
        back.callRemote(monitor, "write", rule)
    end
end
