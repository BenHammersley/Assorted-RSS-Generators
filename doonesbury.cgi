#!/usr/bin/perl -w
use strict;
use CGI qw(:standard);

use Date::Manip;
use XML::RSS;

my $todays_date = &UnixDate("today","%y%m%d");
my $this_year = &UnixDate("today","%Y");

my $rss = XML::RSS->new();
$rss -> channel(title => "Doonesbury");
$rss -> add_item(
    title => "Doonesbury for $todays_date",
    link => "http://images.ucomics.com/comics/db/$this_year/db$todays_date.gif",
    description => '&lt;img src="http://images.ucomics.com/comics/db/2004/'."db$todays_date.gif".'"/&gt;'
        );
                     
print header('application/xml+rss');
print $rss->as_string;
