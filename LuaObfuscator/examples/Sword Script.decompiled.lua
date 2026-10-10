local R0, R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16
R0 = string
R0 = R0.char
R1 = string
R1 = R1.byte
R2 = string
R2 = R2.sub
R3 = bit32
R3 = R3 or bit
R4 = R3.bxor
R5 = table
R5 = R5.concat
R6 = table
R6 = R6.insert
function R7(R0, R1)
  local R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20
  R2 = {}
  R3 = 1
  R4 = #R0
  R5 = 1
  if not (R5 <= 0) then
    if not (R3 > R4) then
      R6 = R3
      elseif not (R3 < R4) then
        R6 = R3
        R7 = _UPVALUE0_
        R8 = R2
        R9 = _UPVALUE1_
        R10 = _UPVALUE2_
        R11 = _UPVALUE3_
        R12 = _UPVALUE4_
        R13 = R0
        R14 = R6
        R15 = R6 + 1
        R20 = R12(R13, R14, R15)
        R11 = R11(R12, R13, R14, R15, R16, R17, R18, R19, R20)
        R12 = _UPVALUE3_
        R13 = _UPVALUE4_
        R14 = R1
        R15 = #R1
        R15 = R6 % R15
        R15 = 1 + R15
        R16 = #R1
        R16 = R6 % R16
        R16 = 1 + R16
        R16 = R16 + 1
        R20 = R13(R14, R15, R16)
        R20 = R12(R13, R14, R15, R16, R17, R18, R19, R20)
        R10 = R10(R11, R12, R13, R14, R15, R16, R17, R18, R19, R20)
        R10 = R10 % 256
        R20 = R9(R10)
        R7(R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20)
      end
    end
  R3 = _UPVALUE5_
  R4 = R2
  return R3(R4, R5, R6)
end
R8 = string
R8 = R8.match
R9 = tonumber
R10 = pcall
function R11()
  local R0, R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11
  repeat
    function R0(R0)
      local R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27
      if R0 then
        R1 = game
        R4 = R0
        R3 = R0[R0]
        R4 = Players
        R5 = "\000\000\000\000"
        R3 = "gui"
        function R3(R0, R1)
          local R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54, R55, R56, R57, R58, R59, R60, R61, R62, R63, R64
          R2 = 0
          R3, R4, R5, R6, R7, R8 = nil, nil, nil, nil, nil, nil
          while true do
            if R2 == 5 then
              R9 = 0
              while true do
                if R9 == 3 then
                  R2 = 6
                  break
                end
                if R9 == 0 then
                  R7.ScrollingEnabled = false
                  R7.Parent = R4
                  R9 = 1
                end
                if R9 == 2 then
                  R10 = Enum
                  R10 = R10.SortOrder
                  R10 = R10.LayoutOrder
                  R8.SortOrder = R10
                  R10 = UDim
                  R10 = R10.new
                  R11 = 0
                  R12 = 1
                  R10 = R10(R11, R12)
                  R8.Padding = R10
                  R9 = 3
                end
                if R9 == 1 then
                  R10 = Instance
                  R11 = _UPVALUE0_
                  R12 = "UIListLayout"
                  R13 = "\000\000\000\000\000\000\000\000"
                  R64 = R11(R12, R13)
                  R10 = R10(R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54, R55, R56, R57, R58, R59, R60, R61, R62, R63, R64)
                  R8 = R10
                  R10 = Enum
                  R10 = R10.HorizontalAlignment
                  R10 = R10.Center
                  R8.HorizontalAlignment = R10
                  R9 = 2
                end
              end
            end
            if R2 == 1 then
              R9 = 0
              while true do
                if R9 == 1 then
                  R4.BorderSizePixel = 1
                  R4.Active = true
                  R9 = 2
                end
                if R9 == 0 then
                  R10 = Color3
                  R10 = R10.fromRGB
                  R11 = 46
                  R12 = 46
                  R13 = 46
                  R10 = R10(R11, R12, R13)
                  R4.BackgroundColor3 = R10
                  R10 = Color3
                  R10 = R10.new
                  R11 = 0
                  R12 = 0
                  R13 = 0
                  R10 = R10(R11, R12, R13)
                  R4.BorderColor3 = R10
                  R9 = 1
                end
                if R9 == 3 then
                  R2 = 2
                  break
                end
                if R9 == 2 then
                  R4.Parent = R3
                  R10 = Instance
                  R10 = R10.new
                  R11 = _UPVALUE0_
                  R12 = "UICorner"
                  R13 = "\000\000\000\000\000\000"
                  R64 = R11(R12, R13)
                  R10 = R10(R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54, R55, R56, R57, R58, R59, R60, R61, R62, R63, R64)
                  R5 = R10
                  R9 = 3
                end
              end
            end
            if R2 == 3 then
              R6.BorderSizePixel = 1
              R9 = R1 and R9(R10, R11)
              R6.Text = R9
              R9 = R25[R0]
              R11 = 1
              R9 = 2
              R6.TextSize = 20
            end
            if 6 == R2 then
              R8.Parent = R7
              R9 = R3
              R10 = R7
            end
            if R2 == 4 then
              R6.Parent = R4
              R9 = R9.new
              R10 = _UPVALUE0_
              R11 = "ScrollingFrame"
              R12 = "\000\000\000\000\000\000\000"
              R64 = R10(R11, R12)
              R9 = R9(R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54, R55, R56, R57, R58, R59, R60, R61, R62, R63, R64)
              R7 = R9
              R9 = UDim2
              R9 = R9.new
              R10 = 1
              R11 = 0
              R12 = 1
              R13 = -30
              R9 = R9(R10, R11, R12, R13)
              R7.Size = R9
              R9 = UDim2
              R9 = R9.new
              R10 = 0
              R11 = 0
              R12 = 0
              R13 = 30
              R9 = R9(R10, R11, R12, R13)
              R7.Position = R9
              R7.BackgroundTransparency = 1
              R7.ScrollBarThickness = 0
              R2 = 5
            end
            if R2 == 2 then
              R9 = 0
              while true do
                if R9 == 3 then
                  R2 = 3
                  break
                end
                if R9 == 0 then
                  R10 = UDim
                  R10 = R10.new
                  R11 = 0
                  R12 = 5
                  R10 = R10(R11, R12)
                  R5.CornerRadius = R10
                  R5.Parent = R4
                  R9 = 1
                end
                if R9 == 1 then
                  R10 = Instance
                  R11 = _UPVALUE0_
                  R12 = "TextLabel"
                  R13 = "\000\000\000\000\000\000\000\000"
                  R64 = R11(R12, R13)
                  R10 = R10(R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54, R55, R56, R57, R58, R59, R60, R61, R62, R63, R64)
                  R6 = R10
                  R10 = UDim2
                  R10 = R10.new
                  R11 = 1
                  R12 = 0
                  R13 = 0
                  R14 = 30
                  R10 = R10(R11, R12, R13, R14)
                  R6.Size = R10
                  R9 = 2
                end
                if R9 == 2 then
                  R10 = UDim2
                  R10 = R10.new
                  R11 = 0
                  R12 = 0
                  R13 = 0
                  R14 = 0
                  R10 = R10(R11, R12, R13, R14)
                  R6.Position = R10
                  R10 = Color3
                  R10 = R10.new
                  R11 = 0
                  R12 = 0
                  R13 = 0
                  R10 = R10(R11, R12, R13)
                  R6.BackgroundColor3 = R10
                  R9 = 3
                end
              end
            end
            if R2 == 0 then
              R9 = 0
              repeat
                if R9 == 2 then
                  R10 = UDim2
                  R10 = R10.new
                  R11 = 0
                  R12 = 150
                  R13 = 0
                  R14 = 200
                  R10 = R10(R11, R12, R13, R14)
                  R4.Size = R10
                  R10 = UDim2
                  R10 = R10.new
                  R11 = 0
                  R12 = 0
                  R13 = 0.2
                  R14 = 0
                  R10 = R10(R11, R12, R13, R14)
                  R4.Position = R10
                  R9 = 3
                end
                if R9 == 1 then
                  R3.ResetOnSpawn = false
                  R10 = Instance
                  R10 = R10.new
                  R11 = _UPVALUE0_
                  R12 = "Frame"
                  R13 = "\000\000\000\000\000\000"
                  R64 = R11(R12, R13)
                  R10 = R10(R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54, R55, R56, R57, R58, R59, R60, R61, R62, R63, R64)
                  R4 = R10
                  R9 = 2
                end
                if R9 == 3 then
                  R2 = 1
                else
                  R10 = Instance
                  R11 = _UPVALUE0_
                  R12 = "ScreenGui"
                  R11 = R13[R0]
                  R3 = "SortOrder"
                  R64 = R10()
                  R10[R10] = R60
                  R9 = R8
                end
              until R9 == 0
            end
          end
        end
        R2.gui = R3
        function R3(R0, R1, R2)
          local R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49, R50
          R3 = 0
          R4, R5, R6, R7, R8, R9 = nil, nil, nil, nil, nil, nil
          while true do
            if R3 == 0 then
              R4 = 0
              R5 = nil
              R3 = 1
            end
            if R3 == 3 then
              while true do
                R10 = 0
                while true do
                  if 1 == R10 then
                    if 3 == R4 then
                      R11 = 0
                      while true do
                        if R11 == 1 then
                          R12 = Enum
                          R12 = R12.TextXAlignment
                          R12 = R12.Left
                          R6.TextXAlignment = R12
                          R4 = 4
                          break
                        end
                        if R11 == 0 then
                          R12 = Enum
                          R12 = R12.Font
                          R12 = R12.GothamBold
                          R6.Font = R12
                          R6.TextSize = 16
                          R11 = 1
                        end
                      end
                    end
                    if R4 == 5 then
                      R11 = Instance
                      R12 = _UPVALUE0_
                      R13 = "TextBox"
                      R14 = "\000\000\000\000"
                      R50 = R12(R13, R14)
                      R11 = R11(R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49, R50)
                      R8 = R11
                      R11 = UDim2
                      R11 = R11.new
                      R12 = 0
                      R13 = 44
                      R14 = 0
                      R15 = 26
                      R11 = R11(R12, R13, R14, R15)
                      R8.Size = R11
                      R11 = UDim2
                      R11 = R11.new
                      R12 = 0
                      R13 = 100
                      R14 = 0
                      R15 = 3
                      R11 = R11(R12, R13, R14, R15)
                      R8.Position = R11
                      R4 = 6
                    end
                    R10 = 2
                  end
                  if 3 == R10 then
                    if 7 == R4 then
                      R11 = 0
                      while true do
                        if R11 == 0 then
                          R12 = Enum
                          R12 = R12.Font
                          R12 = R12.Code
                          R8.Font = R12
                          R8.TextSize = 15
                          R11 = 1
                        end
                        if R11 == 1 then
                          R8.Parent = R5
                          R4 = 8
                          break
                        end
                      end
                    end
                    if R4 == 9 then
                      R11 = 0
                      while true do
                        if R11 == 0 then
                          R12 = R8.FocusLost
                          R13 = R12
                          R12 = R12.Connect
                          function R14(R0)
                            local R1, R2, R3, R4, R5, R6, R7
                            if R0 then
                              R1 = _UPVALUE0_
                              if R1 then
                                R1 = _UPVALUE0_
                                R2 = _UPVALUE1_
                                R2 = R2.Text
                                R1(R2)
                              end
                            end
                          end
                          R12(R13, R14)
                          return R5
                        end
                      end
                    end
                    R10 = 4
                  end
                  if R10 == 4 then
                    if 1 == R4 then
                      R11 = 0
                      while true do
                        if R11 == 0 then
                          R5.Parent = R0
                          R12 = Instance
                          R12 = R12.new
                          R13 = _UPVALUE0_
                          R14 = "TextLabel"
                          R15 = "\000\000\000\000\000\000\000"
                          R50 = R13(R14, R15)
                          R12 = R12(R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49, R50)
                          R6 = R12
                          R11 = 1
                        end
                        if R11 == 1 then
                          R12 = UDim2
                          R12 = R12.new
                          R13 = 1
                          R14 = 0
                          R15 = 1
                          R16 = 0
                          R12 = R12(R13, R14, R15, R16)
                          R6.Size = R12
                          R4 = 2
                          break
                        end
                      end
                    end
                    if R4 == 6 then
                      R11 = 0
                      while true do
                        if R11 == 0 then
                          R12 = Color3
                          R12 = R12.fromRGB
                          R13 = 60
                          R14 = 60
                          R15 = 60
                          R12 = R12(R13, R14, R15)
                          R8.BackgroundColor3 = R12
                          R8.Text = ""
                          R11 = 1
                        end
                        if R11 == 1 then
                          R12 = Color3
                          R12 = R12.fromRGB
                          R13 = 255
                          R14 = 255
                          R15 = 255
                          R12 = R12(R13, R14, R15)
                          R8.TextColor3 = R12
                          R4 = 7
                          break
                        end
                      end
                    end
                    break
                  end
                  if 0 == R10 then
                    if R4 == 8 then
                      R11 = Instance
                      R12[R0] = R0
                      R12 = "new"
                      R9[R11] = R0
                      R11 = R46[R0]
                      R11 = _UPVALUE13_
                      R9 = "Parent"
                    end
                    if R4 == 2 then
                      R11 = R1 and R11(R12, R13)
                      R6.Text = R11
                      R6.BackgroundTransparency = 1
                      R11 = Color3
                      R11 = R11.fromRGB
                      R12 = 255
                      R13 = 255
                      R14 = 255
                      R11 = R11(R12, R13, R14)
                      R6.TextColor3 = R11
                      R4 = 3
                    end
                    R10 = 1
                  end
                  if R10 == 2 then
                    if R4 == 4 then
                      R11 = 0
                      repeat
                        if R11 == 1 then
                          R12 = UDim
                          R12 = R12.new
                          R13 = 0
                          R14 = 8
                          R12 = R12(R13, R14)
                          R7.PaddingLeft = R12
                          R4 = 5
                        else
                          R6.Parent = R5
                          R12 = R12(R13)
                          R13 = "TextBox"
                        end
                      until R11 == 0
                    end
                    if R4 == 0 then
                      R11 = 0
                      while true do
                        if R11 == 0 then
                          R12 = Instance
                          R13 = _UPVALUE0_
                          R14 = "Frame"
                          R15 = "\000\000\000\000\000\000"
                          R50 = R13(R14, R15)
                          R12 = R12(R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49, R50)
                          R5 = R12
                          R12 = UDim2
                          R12 = R12.new
                          R13 = 1
                          R14 = 0
                          R15 = 0
                          R16 = 32
                          R12 = R12(R13, R14, R15, R16)
                          R5.Size = R12
                          R11 = 1
                        end
                        if 1 == R11 then
                          R5.BackgroundTransparency = 1
                          R4 = 1
                          break
                        end
                      end
                    end
                    R10 = 3
                  end
                end
              end
              break
            end
            if R3 == 1 then
              R6, R7 = nil, nil
              R3 = 2
            end
            if R3 == 2 then
              R8, R9 = nil, nil
              R3 = 3
            end
          end
        end
        function R4(R0, R1, R2)
          local R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45
          R3 = 0
          R4, R5, R6, R7, R8, R9 = nil, nil, nil, nil, nil, nil
          while true do
            R10 = 0
            while true do
              if R10 == 0 then
                if R3 == 4 then
                  R11 = 0
                  while true do
                    if R11 == 2 then
                      R3 = 5
                      break
                    end
                    if R11 == 1 then
                      R12 = Color3
                      R12 = R12.fromRGB
                      R13 = 240
                      R14 = 128
                      R15 = 128
                      R12 = R12(R13, R14, R15)
                      R7.BackgroundColor3 = R12
                      R7.Text = ""
                      R11 = 2
                    end
                    if R11 == 0 then
                      R12 = UDim2
                      R12 = R12.new
                      R13 = 0
                      R14 = 26
                      R15 = 0
                      R16 = 26
                      R12 = R12(R13, R14, R15, R16)
                      R7.Size = R12
                      R12 = UDim2
                      R12 = R12.new
                      R13 = 0
                      R14 = 114
                      R15 = 0
                      R16 = 3
                      R12 = R12(R13, R14, R15, R16)
                      R7.Position = R12
                      R11 = 1
                    end
                  end
                end
                if R3 == 6 then
                  R8.Parent = R7
                  R9 = false
                  R11 = R7.MouseButton1Click
                  R12 = R11
                  R11 = R11.Connect
                  function R13()
                    local R0, R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11
                    R0 = 0
                    R1 = nil
                    while true do
                      if R0 == 0 then
                        R1 = 0
                        while true do
                          if R1 == 0 then
                            R2 = 0
                            while true do
                              if R2 == 0 then
                                R3 = _UPVALUE0_
                                R3 = not R3
                                _UPVALUE0_ = R3
                                R3 = _UPVALUE1_
                                R4 = _UPVALUE0_
                                if R4 then
                                  R4 = Color3
                                  R4 = R4.fromRGB
                                  R5 = 152
                                  R6 = 255
                                  R7 = 152
                                  R4 = R4(R5, R6, R7)
                                elseif not R4 then
                                  R4 = Color3
                                  R4 = R4.fromRGB
                                  R5 = 240
                                  R6 = 128
                                  R7 = 128
                                  R4 = R4(R5, R6, R7)
                                end
                                R3.BackgroundColor3 = R4
                                R2 = 1
                              end
                              if 1 == R2 then
                                R1 = 1
                                break
                              end
                            end
                          end
                          if R1 == 1 then
                            R2 = _UPVALUE2_
                            if R2 then
                              R2 = _UPVALUE2_
                              R3 = _UPVALUE0_
                              R2(R3)
                            end
                            break
                          end
                        end
                        break
                      end
                    end
                  end
                  R11(R12, R13)
                  return R4
                end
                R10 = 1
              end
              if R10 == 2 then
                if R3 == 1 then
                  R11 = 0
                  while true do
                    if 1 == R11 then
                      R12 = R1 and R12(R13, R14)
                      R5.Text = R12
                      R5.BackgroundTransparency = 1
                      R11 = 2
                    end
                    if 0 == R11 then
                      R12 = Instance
                      R13 = _UPVALUE0_
                      R14 = "TextLabel"
                      R15 = "\000\000\000\000"
                      R45 = R13(R14, R15)
                      R12 = R12(R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45)
                      R5 = R12
                      R12 = UDim2
                      R12 = R12.new
                      R13 = 1
                      R14 = 0
                      R15 = 1
                      R16 = 0
                      R12 = R12(R13, R14, R15, R16)
                      R5.Size = R12
                      R11 = 1
                    end
                    if R11 == 2 then
                      R3 = 2
                      break
                    end
                  end
                end
                if R3 == 0 then
                  R11 = 0
                  while true do
                    if R11 == 2 then
                      R3 = 1
                      break
                    end
                    if R11 == 0 then
                      R12 = Instance
                      R13 = _UPVALUE0_
                      R14 = "Frame"
                      R15 = "\000\000\000\000\000\000\000\000"
                      R45 = R13(R14, R15)
                      R12 = R12(R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45)
                      R4 = R12
                      R12 = UDim2
                      R12 = R12.new
                      R13 = 1
                      R14 = 0
                      R15 = 0
                      R16 = 32
                      R12 = R12(R13, R14, R15, R16)
                      R4.Size = R12
                      R11 = 1
                    end
                    if R11 == 1 then
                      R4.BackgroundTransparency = 1
                      R4.Parent = R0
                      R11 = 2
                    end
                  end
                end
                R10 = 3
              end
              if R10 == 1 then
                if R3 == 3 then
                  R11 = 0
                  repeat
                    if R11 == 1 then
                      R12 = UDim
                      R12 = R12.new
                      R13 = 0
                      R14 = 8
                      R12 = R12(R13, R14)
                      R6.PaddingLeft = R12
                      R12 = Instance
                      R12 = R12.new
                      R13 = _UPVALUE0_
                      R14 = "TextButton"
                      R15 = "\000\000\000\000\000\000\000"
                      R45 = R13(R14, R15)
                      R12 = R12(R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45)
                      R7 = R12
                      R11 = 2
                    end
                    if R11 == 2 then
                      R3 = 4
                    else
                      R5.Parent = R4
                      R12 = R12(R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27)
                      R13 = "new"
                    end
                  until R11 == 0
                end
                if R3 == 5 then
                  R11 = 0
                  while true do
                    if R11 == 1 then
                      R12 = Instance
                      R13 = R0[R0]
                      R14 = "UICorner"
                      R45 = R15(R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41)
                      R13[R15] = R0
                      R8 = ""
                      R12 = R12
                      R12 = "UDim2"
                    end
                    if R11 == 2 then
                      R3 = 6
                      break
                    end
                    if R11 == 0 then
                      R12 = Color3
                      R12 = R12.new
                      R13 = 255
                      R14 = 255
                      R15 = 255
                      R12 = R12(R13, R14, R15)
                      R7.TextColor3 = R12
                      R7.Parent = R4
                      R11 = 1
                    end
                  end
                end
                R10 = 2
              end
              if R10 == 3 then
                if R3 == 2 then
                  R11 = 0
                  while true do
                    if R11 == 1 then
                      R5.TextSize = 16
                      R12 = Enum
                      R12 = R12.TextXAlignment
                      R12 = R12.Left
                      R5.TextXAlignment = R12
                      R11 = 2
                    end
                    if R11 == 2 then
                      R3 = 3
                      break
                    end
                    if R11 == 0 then
                      R12 = Color3
                      R12 = R12.new
                      R13 = 255
                      R14 = 255
                      R15 = 255
                      R12 = R12(R13, R14, R15)
                      R5.TextColor3 = R12
                      R12 = Enum
                      R12 = R12.Font
                      R12 = R12.GothamBold
                      R5.Font = R12
                      R11 = 1
                    end
                  end
                end
                break
              end
            end
          end
        end
        R6 = R2
        R5 = R2.gui
        R27 = R8(R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27)
        R9 = "\000\000\000\000\000\000\000"
        R7 = true
        R7 = 0
        R27 = R8()
        R27 = R11()
        R13 = _UPVALUE0_
        R14 = "Players"
        R13 = "\159\224\199\167\1557"
        R11 = R11.LocalPlayer
        function R13(R0)
          local R1, R2, R3, R4, R5, R6, R7, R8, R9
          R4 = R0
          R3 = R0[R0]
          R4 = HumanoidRootPart
          R5 = "\000\000\000\000\000\000\000\000"
          R3 = "\000\000\000\000\000\000\000\000"
          do  end
          R2 = R0
          R1 = R0.FindFirstChild
          R9 = R1()
          if not R1 then
            R2 = R0
            R1 = R0.FindFirstChild
            R9 = R1()
          end
          return R1
        end
        function R14()
          local R0, R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11
          R0 = _UPVALUE0_
          if R0 then
            R0 = _UPVALUE1_
            R0 = R0.Character
            if R0 then
              R0 = 0
              R1 = nil
              while true do
                if 0 == R0 then
                  R1 = 0
                  while true do
                    if R1 == 0 then
                      R2 = Instance
                      R2 = 0
                      _UPVALUE3_ = R3
                      R5["\000\000\000\000"] = R0
                      R3 = "BodyAngularVelocity"
                      R11 = R2()
                      R2 = 0
                      R3 = "Instance"
                      R5 = _g_8_a8ab1744349d53
                    end
                    if R1 == 2 then
                      R2 = _UPVALUE2_
                      R3 = _UPVALUE4_
                      R4 = _UPVALUE1_
                      R4 = R4.Character
                      R3 = R3(R4)
                      R2.Parent = R3
                      break
                    end
                    if 1 == R1 then
                      R2 = 0
                      while true do
                        if R2 == 0 then
                          R3 = _UPVALUE2_
                          R4 = Vector3
                          R4 = R4.new
                          R5 = 0
                          R6 = math
                          R6 = R6.huge
                          R7 = 0
                          R4 = R4(R5, R6, R7)
                          R3.MaxTorque = R4
                          R3 = _UPVALUE2_
                          R4 = Vector3
                          R4 = R4.new
                          R5 = 0
                          R6 = _UPVALUE5_
                          R7 = 0
                          R4 = R4(R5, R6, R7)
                          R3.AngularVelocity = R4
                          R2 = 1
                        end
                        if R2 == 1 then
                          R1 = 2
                          break
                        end
                      end
                    end
                  end
                  break
                end
              end
            end
          end
        end
        R15 = R3
        R16 = R6
        R17 = _UPVALUE0_
        R18 = "Range"
        R19 = "\000\000\000\000\000\000\000"
        R17 = R17(R18, R19)
        function R18(R0)
          local R1, R2, R3, R4, R5, R6, R7
          R1 = tonumber
          R2 = R0
          R1 = R1(R2)
          _UPVALUE0_ = R1
        end
        R15(R16, R17, R18)
        R15 = R4
        R16 = R6
        R17 = _UPVALUE0_
        R18 = "Kill Aura"
        R19 = "\159\224\199\167\1557"
        R17 = R17(R18, R19)
        function R18(A0_0)
          local L1_1, L2_2, L3_3, L4_4, L5_5, L6_6, L7_7
          _UPVALUE0_ = A0_0
        end
        R15(R16, R17, R18)
        R15 = R3
        R16 = R6
        R17 = _UPVALUE0_
        R18 = "Spin Speed"
        R19 = "\000\000\000\000"
        R17 = R17(R18, R19)
        function R18(R0)
          local R1, R2, R3, R4, R5, R6, R7, R8, R9, R10
          R1 = 0
          while true do
            if R1 == 0 then
              R2 = tonumber
              R3 = R0
              R2 = R2(R3)
              _UPVALUE0_ = R2
              R2 = _UPVALUE1_
              if R2 then
                R2 = _UPVALUE1_
                R3 = Vector3
                R3 = R3.new
                R4 = 0
                R5 = _UPVALUE0_
                R6 = 0
                R3 = R3(R4, R5, R6)
                R2.AngularVelocity = R3
              end
              break
            end
          end
        end
        R15(R16, R17, R18)
        R15 = R4
        R16 = R6
        R17 = _UPVALUE0_
        R18 = "Spin"
        R19 = "\000\000\000\000\000\000\000"
        R17 = R17(R18, R19)
        function R18(R0)
          local R1, R2, R3, R4, R5, R6, R7, R8, R9, R10
          R1 = 0
          R2 = nil
          while true do
            if R1 == 0 then
              R2 = 0
              while true do
                if R2 == 0 then
                  _UPVALUE0_ = R0
                  R3 = _UPVALUE0_
                  if R3 then
                    R3 = _UPVALUE1_
                    R3()
                    break
                  end
                  R3 = _UPVALUE2_
                  if R3 then
                    R3 = 0
                    R4 = nil
                    while true do
                      if R3 == 0 then
                        R4 = 0
                        while true do
                          if R4 == 0 then
                            R5 = _UPVALUE2_
                            R5(R6)
                          end
                        end
                        break
                      end
                    end
                  end
                  break
                end
              end
              break
            end
          end
        end
        R15(R16, R17, R18)
        R15 = R11.CharacterAdded
        R16 = R15
        R15 = R15.Connect
        function R17(R0)
          local R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11
          R1 = 0
          R2 = nil
          while true do
            if R1 == 0 then
              R2 = 0
              while true do
                if R2 == 1 then
                  R3 = _UPVALUE0_
                  if R3 then
                    R3 = _UPVALUE1_
                    R3()
                  end
                  break
                end
                if R2 == 0 then
                  R4 = R0
                  R3 = R0.WaitForChild
                  R5 = 1
                  R7 = _g_4_3b4a4eb5
                  R11 = R3()
                  do break end
                  R3 = 0
                  while true do
                    if R3 == 0 then
                      R4 = _UPVALUE3_
                      R4(R5)
                    end
                  end
                  R2 = 1
                end
              end
              break
            end
          end
        end
        R15 = _UPVALUE15_
        R19 = R23[R0]
        R27 = R15()
        function R17()
          local R0, R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25
          R0 = _UPVALUE0_
          if R0 then
            R0 = 0
            R1 = nil
            while true do
              if 0 == R0 then
                R2 = game
                R2 = R2
                R4 = 1
                R6 = R1[R5]
                R6 = R6.Character
                if R6 then
                  R8 = R6
                  R7 = R6.FindFirstChild
                  R9 = _UPVALUE1_
                  R10 = "Humanoid"
                  R11 = "\000\000\000\000\000\000"
                  R25 = R9(R10, R11)
                  R7 = R7(R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25)
                  if R7 then
                    R7 = R6.Humanoid
                    R7 = R7.Health
                    if R7 > 0 then
                      R8 = R6
                      R7 = R6.FindFirstChild
                      R9 = _UPVALUE1_
                      R10 = "HumanoidRootPart"
                      R11 = "\000\000\000\000\000\000\000\000"
                      R25 = R9(R10, R11)
                      R7 = R7(R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25)
                      if R7 then
                        R7 = _UPVALUE2_
                        R9 = R3
                        R8 = R3[R0]
                        do break end
                        R7 = 0
                        R8, R9 = nil, nil
                        while true do
                          repeat
                            if R7 == 0 then
                              R8 = 0
                              R9 = nil
                              R7 = 1
                            end
                          until R7 == 1
                          while true do
                            if R8 == 0 then
                              R10 = _UPVALUE2_
                              R10 = R10.Character
                              R9 = R10 or R10
                              if R9 then
                                R11 = R9
                                R10 = R9.FindFirstChild
                                R12 = _UPVALUE1_
                                R13 = "Handle"
                                R14 = "\000\000\000\000\000"
                                R25 = R12(R13, R14)
                                R10 = R10(R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25)
                                if R10 then
                                  R10 = 0
                                  while true do
                                    if 0 == R10 then
                                      R12 = R9
                                      R11 = R9.Activate
                                      R12 = _UPVALUE13_
                                      R25 = R0(R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25)
                                      while true do
                                        R17 = R15
                                        R16 = R15.IsA
                                        R18 = _UPVALUE1_
                                        R19 = "BasePart"
                                        R20 = "\000\000\000\000\000\000\000\000"
                                        R25 = R18(R19, R20)
                                        R16 = R16(R17, R18, R19, R20, R21, R22, R23, R24, R25)
                                        if R16 then
                                          R16 = 0
                                          R17 = nil
                                          while true do
                                            if R16 == 0 then
                                              R17 = 0
                                              while true do
                                                if R17 == 0 then
                                                  R18 = firetouchinterest
                                                  R19 = R9.Handle
                                                  R20 = R15
                                                  R21 = 0
                                                  R18(R19, R20, R21)
                                                  R18 = firetouchinterest
                                                  R19 = R9.Handle
                                                  R20 = R15
                                                  R21 = 1
                                                  R18(R19, R20, R21)
                                                  break
                                                end
                                              end
                                              break
                                            end
                                          end
                                        end
                                      end
                                      break
                                    end
                                  end
                                end
                              end
                              break
                            end
                          end
                          break
                        end
                      end
                    end
                  end
                end
                break
              end
            end
          end
        end
        R15(R16, R17)
      else
        R1 = R0[1]
      end
    end
    R2 = _UPVALUE2_
    R3 = _UPVALUE2_
    R4 = {R5}
    R5 = _UPVALUE3_
    R6 = R0
    R7 = nil
    R11 = R5(R6, R7)
    ;({R5})[2] = R6
    ;({R5})[3] = R7
    ;({R5})[4] = R8
    ;({R5})[5] = R9
    ;({R5})[6] = R10
    ;({R5})[7] = R11
    R4 = R4[2]
    R11 = R2(R3, R4)
  until R1 == R2
  do  end
  R1 = R0
  R2 = {}
  do return R1(R2) end
  do  end
  R1 = _UPVALUE4_
  return R1(R2, R3, R4, R5, R6, R7, R8, R9, R10, R11)
end
R12 = R11
return R12(R13, R14, R15, R16)
