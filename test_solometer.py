import lupa, pathlib

L = lupa.LuaRuntime()
L.execute(r"""
Enum = { DamageMeterType = { DamageDone = 0, EnemyDamageTaken = 9 } }
UnitName = function() return "Sam" end
function hooksecurefunc(t, k, fn) local o = t[k]; t[k] = function(...) local r = o(...); fn(...); return r end end
EventUtil = { ContinueOnAddOnLoaded = function(_, fn) fn() end }
local function region() return { SetText = function(s, t) s.text = t end } end
function frame(isMe, h)
  local bar = { Name = region(), SetMinMaxValues = function(s, a, b) s.max = b end, SetValue = function(s, v) s.val = v end }
  return { isLocalPlayer = isMe, shown = true, IsShown = function(s) return s.shown end,
    SetAlpha = function(s, a) s.alpha = a end, EnableMouse = function(s, m) s.mouse = m end, GetStatusBar = function() return bar end,
    ClearAllPoints = function(s) s.y = nil end, SetPoint = function(s, _, _, _, _, y) s.y = y end, GetHeight = function() return h or 20 end }
end
mate, me, pinned = frame(false), frame(true), frame(true)
pinned.shown = false
win = { type = 0, frames = { mate, me } }
function win:IsEditing() return false end
function win:GetDamageMeterType() return self.type end
function win:IsNonInteractive() return false end
function win:GetBarSpacing() return 2 end
function win:GetLocalPlayerEntry() return pinned end
function win:GetScrollBar() return { SetAlpha = function() end } end
function win:GetScrollBox() return { ForEachFrame = function(_, fn) for _, f in ipairs(win.frames) do fn(f) end end } end
function win:InitEntry(f) end
function win:EnsureLocalPlayerPresent() end
function win:GetBarHeight() return 20 end
function win:GetHeader() return { GetHeight = function() return 32 end } end
function win:SetHeight(h) self.h = h end
function win:ClearAllPoints() self.points = {} end
function win:SetPoint(p) self.points[#self.points + 1] = p end
DamageMeter = { windowDataList = { { sessionWindow = win } }, SetupSessionWindow = function() end,
  GetPrimarySessionWindow = function() return win end }
""")
L.execute(pathlib.Path(__file__).with_name("SoloMeter.lua").read_text())
g = L.globals()

assert g.mate.alpha == 0 and g.mate.mouse is False, "teammate row must be hidden and unclickable"
assert g.me.alpha == 1 and g.me.y == 0, "your row must show at the top"
assert g.me.GetStatusBar().Name.text == "Sam" and g.me.GetStatusBar().max == 1, "rank and relative bar must be gone"
assert g.pinned.alpha == 0, "pinned row hidden while your real row is visible"
assert g.win.h == 32 + 8 + 20, "window shrinks to header + one row"
assert list(g.win.points.values()) == ["TOPLEFT", "TOPRIGHT"], "main window pinned by its top only"

g.win.frames = L.eval("{ mate }"); g.pinned.shown = True
g.win.EnsureLocalPlayerPresent(g.win)
assert g.pinned.alpha == 1 and g.pinned.y == 0, "pinned row takes the top slot"

g.win.type = 9
g.win.InitEntry(g.win, g.mate)
assert g.mate.alpha == 1, "enemy rows stay visible"
g.win.EnsureLocalPlayerPresent(g.win)
assert list(g.win.points.values()) == ["TOPLEFT", "BOTTOMRIGHT"], "main window back to the Edit Mode size"
print("ok")
