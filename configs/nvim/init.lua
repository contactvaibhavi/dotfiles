local function get_python_path()
  local venv = os.getenv("VIRTUAL_ENV")
  if venv then
    return venv .. "/bin/python"
  end

  local handle = io.popen("pyenv which python 2>/dev/null")
  if handle then
    local result = handle:read("*a")
    handle:close()
    return result:gsub("%s+", "")
  end

  return "python3" -- fallback
end

vim.g.python3_host_prog = get_python_path()

-- Let python-mode initialize properly
vim.g.pymode_python = "python3"
vim.g.pymode_virtualenv = 1

-- bootstrap lazy.nvim, LazyVim and your plugins
require("config.lazy")
-- vim.g.python3_host_prog = vim.fn.expand("~/.config/nvim/venv/bin/python")
vim.keymap.set("v", "<C-c>", '"+y')
vim.opt.clipboard = "unnamedplus"
vim.opt.clipboard = "unnamedplus"
vim.keymap.set("v", "<D-c>", '"+y')
vim.keymap.set("i", "<D-v>", "<C-r>+")

-- Add this anywhere in the file
vim.g.clipboard = {
  name = "pbcopy",
  copy = {
    ["+"] = "pbcopy",
    ["*"] = "pbcopy",
  },
  paste = {
    ["+"] = "pbpaste",
    ["*"] = "pbpaste",
  },
  cache_enabled = 0,
}
vim.opt.clipboard = "unnamed"
vim.opt.termguicolors = true
