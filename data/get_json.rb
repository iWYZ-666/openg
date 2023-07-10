# frozen_string_literal: true

require 'open3'

names = ''
File.open('names.txt', 'r') { |f| names = f.read }
names = names.split(',')
names.each do |name|
  (2020..2023).each do |year|
    (1..12).each do |month|
      uri = format("https://oss.x-lab.info/open_digger/github/#{name}/project_openrank_detail/#{year}-%02d.json", month)
      file_name = "#{name}.#{year}-#{month}.json"
      file_name.gsub!('/', '-')
      Open3.capture2("wget #{uri} -O #{file_name}")
    end
  end
end


