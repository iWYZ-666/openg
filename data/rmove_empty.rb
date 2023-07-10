# frozen_string_literal: true

files = Dir.children(File.dirname(__FILE__ ))
files.each do |f|
  next unless File.exist?(f)

  File.delete(f) if File.zero?(f)
end
