local R0, R1, R2, R3, R4, R5, R6, R7, R8, R9, R10
R0 = 0
while true do
  if R0 == 1 then
    R1 = Tab
    R2 = R1
    R1 = R1.CreateButton
    R3 = {}
    R3.Name = "Instant Win"
    function R4()
      local R0, R1, R2, R3, R4, R5, R6, R7
      R0 = getStage
      R1 = 5000
      R0(R1)
    end
    R3.Callback = R4
    R1 = R1(R2, R3)
    Button = R1
    R1 = Tab
    R2 = R1
    R1 = R1.CreateButton
    R3 = {}
    R3.Name = "Next Stage"
    function R4()
      local R0, R1, R2, R3, R4, R5, R6, R7
      R0 = getStage
      R1 = game
      R2 = R1
      R1 = R1.GetService
      R3 = "Players"
      R1 = R1(R2, R3)
      R1 = R1.LocalPlayer
      R1 = R1.leaderstats
      R1 = R1.Stage
      R1 = R1.Value
      R1 = R1 + 1
      R0(R1)
    end
    R3.Callback = R4
    R1 = R1(R2, R3)
    Button = R1
    R1 = Tab
    R2 = R1
    R1 = R1.CreateToggle
    R3 = {}
    R3.Name = "Auto Stage"
    R3.CurrentValue = false
    R3.Flag = "Toggle1"
    function R4(R0)
      local R1, R2, R3, R4, R5, R6, R7, R8, R9
      R1 = 0
      R2 = nil
      while true do
        if R1 == 0 then
          R2 = 0
          while true do
            if R2 == 0 then
              Stage = R0
              R3 = game
              R4 = R3
              R3 = R3.GetService
              R5 = "RunService"
              R3 = R3(R4, R5)
              R3 = R3.Heartbeat
              R4 = R3
              R3 = R3.Connect
              function R5()
                local R0, R1, R2, R3, R4, R5, R6, R7
                R0 = Stage
                if R0 then
                  R0 = game
                  R1 = R0
                  R0 = R0.GetService
                  R2 = "Players"
                  R0 = R0(R1, R2)
                  R0 = R0.LocalPlayer
                  R0 = R0.Character
                  if R0 then
                    R0 = getStage
                    R1 = game
                    R2 = R1
                    R1 = R1.GetService
                    R3 = "Players"
                    R1 = R1(R2, R3)
                    R1 = R1.LocalPlayer
                    R1 = R1.leaderstats
                    R1 = R1.Stage
                    R1 = R1.Value
                    R1 = R1 + 1
                    R0(R1)
                  end
                else
                  R0 = StageHeart
                  R1 = R0
                  R0 = R0.Disconnect
                  R0(R1)
                end
              end
              R3 = R3(R4, R5)
              StageHeart = R3
              break
            end
          end
          break
        end
      end
    end
    R3.Callback = R4
    R1 = R1(R2, R3)
    Toggle = R1
    R0 = 2
  end
  if R0 == 4 then
    function R1(R0)
      local R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16
      R1 = ipairs
      R2 = workspace
      R2 = R2.PointFolder
      R3 = R2
      R2 = R2.GetChildren
      R16 = R2(R3)
      R16 = R1(R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16)
      while true do
        R6 = R5.Name
        R7 = tostring
        R8 = R0
        R7 = R7(R8)
        if R6 == R7 then
          R6 = game
          R7 = R6
          R6 = R6.GetService
          R8 = "Players"
          R6 = R6(R7, R8)
          R6 = R6.LocalPlayer
          R6 = R6.Character
          R7 = R6
          R6 = R6.PivotTo
          R9 = R5
          R8 = R5.GetPivot
          R8 = R8(R9)
          R9 = CFrame
          R9 = R9.new
          R10 = 0
          R11 = 5
          R12 = 0
          R9 = R9(R10, R11, R12)
          R8 = R8 * R9
          R6(R7, R8)
        end
      end
    end
    getStage = R1
    function R1()
      local R0, R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13
      R0 = ipairs
      R1 = workspace
      R1 = R1["stage badge"]
      R2 = R1
      R1 = R1.GetChildren
      R13 = R1(R2)
      R13 = R0(R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13)
      while true do
        R5 = 0
        while true do
          if R5 == 0 then
            R6 = game
            R7 = R6
            R6 = R6.GetService
            R8 = "Players"
            R6 = R6(R7, R8)
            R6 = R6.LocalPlayer
            R6 = R6.Character
            R7 = R6
            R6 = R6.PivotTo
            R9 = R4
            R8 = R4.GetPivot
            R13 = R8(R9)
            R6(R7, R8, R9, R10, R11, R12, R13)
            R6 = task
            R6 = R6.wait
            R7 = 0.1
            R6(R7)
            break
          end
        end
      end
    end
    getBadge = R1
    break
  end
  if R0 == 0 then
    R1 = loadstring
    R2 = game
    R3 = R2
    R2 = R2.HttpGet
    R4 = "https://sirius.menu/rayfield"
    R10 = R2(R3, R4)
    R1 = R1(R2, R3, R4, R5, R6, R7, R8, R9, R10)
    R1 = R1()
    Rayfield = R1
    R1 = Rayfield
    R2 = R1
    R1 = R1.CreateWindow
    R3 = {}
    R3.Name = "[5000 stage!! ] Effortless Tower"
    R3.LoadingTitle = "KhSaeedHub"
    R3.LoadingSubtitle = "Please, Join discord for more scripts!"
    R4 = {}
    R4.Enabled = true
    R5 = KhSaeedHub
    R4.FolderName = R5
    R4.FileName = "KhSaeedHub"
    R3.ConfigurationSaving = R4
    R4 = {}
    R4.Enabled = true
    R4.Invite = "37xqzu6eBF"
    R4.RememberJoins = true
    R3.Discord = R4
    R3.KeySystem = true
    R4 = {}
    R4.Title = "KhSaeedHub"
    R4.Subtitle = "Key System"
    R4.Note = "https://link-target.net/897280/khsaeed90"
    R4.FileName = "KhSaeedHub"
    R4.SaveKey = true
    R4.GrabKeyFromSite = true
    R5 = {}
    R6 = "https://pastebin.com/raw/QKZGwRWK"
    ;({})[-499207279] = R6
    R3.KeySettings = R4
    R1 = R1(R2, R3)
    Window = R1
    R1 = Window
    R2 = R1
    R1 = R1.CreateTab
    R3 = "Main"
    R4 = 8834748103
    R1 = R1(R2, R3, R4)
    Tab = R1
    R0 = 1
  end
  if R0 == 3 then
    R1 = Tab
    R2 = R1
    R1 = R1.CreateSection
    R3 = "Credits to: KhSaeedHub"
    R1 = R1(R2, R3)
    Section = R1
    R1 = Tab
    R2 = R1
    R1 = R1.CreateButton
    R3 = {}
    R3.Name = "Scriptblox Profile"
    function R4()
      local R0, R1, R2, R3, R4, R5, R6, R7
      R0 = 0
      while true do
        if R0 == 0 then
          R1 = setclipboard
          R2 = "https://scriptblox.com/u/KhSaeed90"
          R1(R2)
          R1 = Rayfield
          R2 = R1
          R1 = R1.Notify
          R3 = {}
          R3.Title = "Link is copied"
          R3.Content = "Check scriptblox profile page for more Scripts!"
          R3.Duration = 5
          R3.Image = 14848261712
          R1(R2, R3)
          break
        end
      end
    end
    R3.Callback = R4
    R1 = R1(R2, R3)
    Button = R1
    R1 = Tab
    R2 = R1
    R1 = R1.CreateButton
    R3 = {}
    R3.Name = "Discord Server"
    function R4()
      local R0, R1, R2, R3, R4, R5, R6, R7
      R0 = 0
      while true do
        if R0 == 0 then
          R1 = setclipboard
          R2 = "https://controlc.com/5572471c"
          R1(R2)
          R1 = Rayfield
          R2 = R1
          R1 = R1.Notify
          R3 = {}
          R3.Title = "Link is copied"
          R3.Content = "Join discord server for more Scripts!"
          R3.Duration = 5
          R3.Image = 14848261712
          R1(R2, R3)
          break
        end
      end
    end
    R3.Callback = R4
    R1 = R1(R2, R3)
    Button = R1
    R0 = 4
  end
  if R0 == 2 then
    R1 = Tab
    R2 = R1
    R1 = R1.CreateSlider
    R3 = {}
    R3.Name = "Stage Slider"
    R4 = {}
    R5 = 1
    R6 = 5000
    ;({})[1077028625] = R5
    ;({})[1077028626] = R6
    R3.Increment = 1
    R3.Suffix = "/ 5000 Stage"
    R3.CurrentValue = 1
    R3.Flag = "Slider1"
    function R4(R0)
      local R1, R2, R3, R4, R5, R6, R7
      R1 = getStage
      R2 = R0
      R1(R2)
    end
    R3.Callback = R4
    R1 = R1(R2, R3)
    Slider = R1
    R1 = Tab
    R2 = R1
    R1 = R1.CreateButton
    R3 = {}
    R3.Name = "Get Some Badges"
    function R4()
      getBadge()
    end
    R3.Callback = R4
    R1 = R1(R2, R3)
    Button = R1
    R1 = Window
    R2 = R1
    R1 = R1.CreateTab
    R3 = "Credits"
    R4 = 14848261712
    R1 = R1(R2, R3, R4)
    Tab = R1
    R0 = 3
  end
end
