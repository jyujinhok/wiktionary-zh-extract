mt = require "moduletest"
json = require "json"

local out = {}
out["dials"] = {}
for key, value in pairs(mt.list) do
    if type(value) == "table" then
        if #value > 0 and value[1] ~= "" then
            out["dials"][key] = value
        end
    else
        out[key] = value
    end
end

print(json.encode(out))