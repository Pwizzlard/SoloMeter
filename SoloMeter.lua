local hooked = {}

local function filtering(win)
  return not win:IsEditing() and win:GetDamageMeterType() ~= Enum.DamageMeterType.EnemyDamageTaken
end

local function apply(win, f)
  local show = f.isLocalPlayer or not filtering(win)
  f:SetAlpha(show and 1 or 0)
  f:EnableMouse(show and not win:IsNonInteractive())
  if show and filtering(win) then
    local bar = f:GetStatusBar()
    bar:SetMinMaxValues(0, 1)
    bar:SetValue(1)
    bar.Name:SetText(UnitName("player"))
  end
end

local function fit(win, rowsHeight)
  if win == DamageMeter:GetPrimarySessionWindow() then
    win:ClearAllPoints()
    win:SetPoint("TOPLEFT")
    win:SetPoint(rowsHeight and "TOPRIGHT" or "BOTTOMRIGHT")
  end
  if rowsHeight then win:SetHeight(win:GetHeader():GetHeight() + 8 + rowsHeight) end
end

local function place(win)
  win:GetScrollBar():SetAlpha(filtering(win) and 0 or 0.3)
  if not filtering(win) then return fit(win) end
  local box, pinned, y = win:GetScrollBox(), win:GetLocalPlayerEntry(), 0
  local function stack(f)
    f:ClearAllPoints()
    f:SetPoint("TOPLEFT", box, "TOPLEFT", 0, -y)
    f:SetPoint("TOPRIGHT", box, "TOPRIGHT", 0, -y)
    y = y + f:GetHeight() + win:GetBarSpacing()
  end
  box:ForEachFrame(function(f) if f.isLocalPlayer then stack(f) end end)
  if y == 0 and pinned:IsShown() then pinned:SetAlpha(1) stack(pinned) else pinned:SetAlpha(0) end
  fit(win, y > 0 and y - win:GetBarSpacing() or win:GetBarHeight())
end

local function hook(win)
  if not win or hooked[win] then return end
  hooked[win] = true
  hooksecurefunc(win, "InitEntry", apply)
  hooksecurefunc(win, "EnsureLocalPlayerPresent", place)
  win:GetScrollBox():ForEachFrame(function(f) apply(win, f) end)
  place(win)
end

EventUtil.ContinueOnAddOnLoaded("Blizzard_DamageMeter", function()
  for _, data in pairs(DamageMeter.windowDataList or {}) do hook(data.sessionWindow) end
  hooksecurefunc(DamageMeter, "SetupSessionWindow", function(_, _, data) hook(data.sessionWindow) end)
end)
