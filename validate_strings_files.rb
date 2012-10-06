#!/usr/local/bin/ruby
# encoding: UTF-8
 
# NOTE: requires ruby 1.9
# MIT license
 
# validate_strings_files.rb
# This script reads through the .strings files in a directory and identifies any bad characters inside,
# both those that ibtool would catch and those that ibtool would miss.
# * ibtool verbal errors: " ' : . / - _ $
# * ibtool silent errors: { } [ ] ; , < > ? \ | = + ! ` ~ @ # % ^ & * ( )
 
require 'FileUtils'
 
# Check for arguments.
if ARGV.length != 1
  puts "Usage: ruby validate_strings_files.rb path_to_strings"
  exit
end
 
# Get path argument and 'cd' to that path.
PATH = ARGV[0]
FileUtils.cd(PATH)
 
def verify_file(file)
  line_number = 0
  is_multi_line_comment = false
 
  # Use general method unless file encoding is UTF-16.
  file_handle = File.new(file, "r")
  # file_handle = File.new(file, "r:UTF-16LE:UTF-8") (See http://blog.grayproductions.net/articles/ruby_19s_three_default_encodings)
   
  puts "VERIFYING FILE #{file}"
  while (!file_handle.eof?)
    has_seen_equals_sign = false
    has_seen_semi_colon = false
    is_single_line_comment = false
    is_string = false
    line_number += 1
    previous_char = nil
    second_previous_char = nil
 
    line = file_handle.readline
    # Use each_char (rather than each_byte) to support unicode.
    line.each_char do |char|
      # Notes:
      # * line can only be 2 strings, N multi-line comments, 1 equals sign (=), 1 semi-colon (;)
      # * ignore character if it's in a string
      # * single-line comments are ended by \n
      # * multi-line comments are ended by */
 
      if is_string || is_single_line_comment || is_multi_line_comment
        if is_string && previous_char != "\\" && char == "\""
          is_string = false
        elsif is_string && second_previous_char == "\\" && previous_char == "\\" && char == "\""
          is_string = false
        elsif is_single_line_comment && char == "\n"
          is_single_line_comment = false
        elsif is_multi_line_comment && previous_char == "*" && char == "/"
          is_multi_line_comment = false
        end
        # Ignore.
      elsif previous_char == nil && char == "/"
        # Ignore.
      elsif previous_char == "/" && char == "/"
        is_single_line_comment = true
      elsif previous_char == "/" && char == "*"
        is_multi_line_comment = true
      elsif !has_seen_equals_sign && char == "="
        has_seen_equals_sign = true
      elsif !has_seen_semi_colon && char == ";"
        has_seen_semi_colon = true
      elsif char == " " ||char == "\n"  || char == "\r"
        # Ignore.
      elsif char == "\""
        is_string = true
      elsif char == "\000"
        # Ignore unicode padding.
      elsif line_number == 1 && previous_char == nil && char == "\377"
        # Ignore unicode file header.
      elsif line_number == 1 && previous_char == nil && char == "\376"
        # Ignore unicode file header.
      else
        puts "#{file} (#{line_number}): #{char}"
      end
       
      if char != "\000" && char != "\377" && char != "\376"
        # Save previous character if it's not unicode padding.
        second_previous_char = previous_char
        previous_char = char
      end
    end
  end
end
 
# Iterate through the current directory.
Dir.entries(".").each do |file|
  filename = file.slice(0,file.length-8)
  extension = file.slice(file.length-8,file.length)
  # Only deal with .strings.
  if (extension == ".strings")
    # Read the file and identify any bad characters.
    verify_file(file)
  end
end