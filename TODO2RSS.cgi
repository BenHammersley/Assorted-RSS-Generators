#!/usr/bin/perl -w
# RSS generator for Code TODO comments

use strict;
use XML::RSS;
use CGI qw(:standard);
use File::Find;

# y'all be wanting to change the next line
my $start_directory = "/Users/ben/Code/";


my $rss = new XML::RSS(version => '0.91');
$rss -> channel(title => "Code TODOs");

find (\&search_and_rss, $start_directory);

sub search_and_rss {

open (CODEFILE, "< $File::Find::name");

while (<CODEFILE>) {
    if ($_ =~ m/TODO/) {
    $rss -> add_item(title => "$File::Find::name",
                     link => "file:\/\/$File::Find::name",
                     description => "$_ at Line $. of $File::Find::name");

#TODO: Put in date code here
                    
                     }
                   }  
close (CODEFILE);
}

print header('application/xml+rss');
print $rss->as_string;