module Commandable
  def install(s)
    queue.install_list << s
  end

  def ppa(s)
    queue.ppa_list << s
  end

  def backup(f)
    queue.backup_list << f
  end
end

