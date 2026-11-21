"use client";

import { Menu } from "@base-ui/react/menu";
import { Check, Monitor, Moon, Settings, Sun } from "lucide-react";
import { SidebarMenuButton } from "@/components/ui/sidebar";
import { useTheme } from "@/components/theme-provider";

export function SettingsMenu() {
  const { theme, setTheme } = useTheme();
  const options = [
    { value: "light", label: "Sáng", icon: Sun },
    { value: "dark", label: "Tối", icon: Moon },
    { value: "system", label: "Theo hệ thống", icon: Monitor },
  ] as const;

  return (
    <Menu.Root>
      <Menu.Trigger render={<SidebarMenuButton className="h-11 gap-3 px-3" />}>
        <Settings className="size-5" />
        <span>Setting</span>
      </Menu.Trigger>
      <Menu.Portal>
        <Menu.Positioner
          side="top"
          align="start"
          sideOffset={8}
          className="z-[60]"
        >
          <Menu.Popup
            aria-label="Màu giao diện"
            className="bg-popover text-popover-foreground w-56 rounded-xl border p-1.5 shadow-lg outline-none"
            onKeyDown={(event) => {
              if (event.key === "Escape") event.stopPropagation();
            }}
          >
            <p className="text-muted-foreground px-3 py-2 text-xs">
              Màu giao diện
            </p>
            <Menu.RadioGroup value={theme} onValueChange={setTheme}>
              {options.map(({ value, label, icon: Icon }) => (
                <Menu.RadioItem
                  key={value}
                  value={value}
                  closeOnClick
                  className="data-highlighted:bg-accent flex cursor-pointer items-center gap-3 rounded-lg px-3 py-2.5 text-sm outline-none"
                >
                  <Icon className="size-4" />
                  <span className="flex-1">{label}</span>
                  <Menu.RadioItemIndicator>
                    <Check className="size-4" />
                  </Menu.RadioItemIndicator>
                </Menu.RadioItem>
              ))}
            </Menu.RadioGroup>
          </Menu.Popup>
        </Menu.Positioner>
      </Menu.Portal>
    </Menu.Root>
  );
}
