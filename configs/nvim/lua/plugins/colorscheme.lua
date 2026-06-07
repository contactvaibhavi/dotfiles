return {
  -- Disable default dark themes
  -- { "folke/tokyonight.nvim", enabled = false },

  { "catppuccin/nvim", enabled = false },

  -- Enable light theme
  {
    "projekt0n/github-nvim-theme",
    enabled = false,
    lazy = false,
    priority = 1000,
    config = function()
      require("github-theme").setup({
        options = {
          theme_style = "light",
        },
      })
      vim.cmd([[colorscheme github_light]])
    end,
  },
  {
    "rose-pine/neovim",
    name = "rose-pine",
    lazy = false, -- load at startup
    priority = 1000,
    config = function()
      require("rose-pine").setup({
        variant = "moon", -- moon = warmest/most muted, main = standard, dawn = light
      })
      vim.cmd.colorscheme("rose-pine")
    end,
  },
}
