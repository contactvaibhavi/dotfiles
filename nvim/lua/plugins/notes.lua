return {
  -- Obsidian integration for notes
  {
    "epwalsh/obsidian.nvim",
    version = "*",
    lazy = true,
    ft = "markdown",
    dependencies = {
      "nvim-lua/plenary.nvim",
      "nvim-telescope/telescope.nvim",
    },
    opts = {
      workspaces = {
        {
          name = "notes",
          path = "~/notes",
        },
        {
          name = "journal",
          path = "~/journal",
        },
      },
      daily_notes = {
        folder = "daily",
        date_format = "%Y-%m-%d",
      },
    },
    keys = {
      { "<leader>on", "<cmd>ObsidianNew<cr>", desc = "New Note" },
      { "<leader>oo", "<cmd>ObsidianSearch<cr>", desc = "Search Notes" },
      { "<leader>ot", "<cmd>ObsidianToday<cr>", desc = "Today's Note" },
    },
  },

  -- Markdown preview
  {
    "iamcco/markdown-preview.nvim",
    cmd = { "MarkdownPreviewToggle", "MarkdownPreview" },
    build = "cd app && npm install",
    ft = { "markdown" },
    keys = {
      { "<leader>mp", "<cmd>MarkdownPreviewToggle<cr>", desc = "Markdown Preview" },
    },
  },
}
