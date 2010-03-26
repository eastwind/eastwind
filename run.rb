#!/usr/bin/env ruby

require 'queue'

queue = Queue.new

require 'command'
Dir["./script/*.rb"].each {|p| require p}

queue.addppa
system "apt-get update"
queue.install

