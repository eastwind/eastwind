class Queue
  attr_accessor :ppa_list, :install_list

  def addppa
    for s in ppa_list
      system "add-apt-repository #{s}"
    end
  end

  def install
    for s in install_list
      system "apt-get install --yes #{s}"
    end
  end

  def backup
    for s in backup_list
      system "cp #{f} ./lib"
    end
  end
end

