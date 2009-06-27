#!/usr/bin/perl -w

# Installed Perl Modules to RSS
# Ben Hammersley, July 2004

use strict;
use CGI qw(:standard);
use XML::RSS;
use ExtUtils::Installed;

my $installed = ExtUtils::Installed->new();
my $machine_name = `uname -n`;

my $rss = new XML::RSS(version => '2.0');
$rss -> channel(title => "Perl Modules on $machine_name");
$rss -> channel(link => "http://www.benhammersley.com/tools/");

foreach my $module ($installed->modules()) {
       my $version = $installed->version($module) || "???";

           $rss -> add_item ( title => "$module $version",
                          description => "$module $version",
                          link => "http://search.cpan.org/search%3fmodule=$module",        
                          );
          }

print header('application/rss+xml');
print $rss->as_string;