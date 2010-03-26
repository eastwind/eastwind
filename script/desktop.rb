class Desktop
  include Commandable

  def before
    ppa "ppa:docky-core/ppa"
  end

  def body
    install "docky"
  end
end

