#!/usr/bin/perl -w
# RSS generator from Kwiki RecentChanges

use lib '/home/ben/web/lib/perl';
use strict;
use XML::RSS;
use CGI qw(:standard);
use LWP::Simple 'get';
use HTML::TokeParser;
use Date::Manip;
my $tag;

my $cgi = CGI::new();

my $url = $cgi->param('url');

my $recent_changes_file = get("$url/csp?RecentChanges");

my $stream = HTML::TokeParser->new( \$recent_changes_file );

my $rss = new XML::RSS(version => '1.0');

$rss -> channel(title => "Recent Changes file for $url",
                link => "$url/csp?RecentChanges",
                description => "The latest changed pages on the EuroFoo wiki",
                    );


$stream->get_tag("table");
$stream->get_tag("/tr");

while ($tag = $stream->get_tag('tr')) {

$stream->get_tag('td');
$stream->get_tag('a');
my $changed_page = $stream->get_text();
$stream->get_tag('td');
my $changed_by = $stream->get_text();
$stream->get_tag('td');
my $edit_time = $stream->get_text();

$edit_time =~ s/ 2004 GMT/+00:00/g;
my $parsed_date = ParseDate($edit_time);
my $w3cdtf_date = UnixDate($parsed_date, "%Y-%m-%dT%H:%M:%S%z");


$rss -> add_item( title => "$changed_page",
                  link => "$url/null?$changed_page",
                  description => "Edited at $edit_time by $changed_by",

                  dc => { creator => "$changed_by",
                          date => "$w3cdtf_date",},

                  );


}

print header('application/xml+rss');
print $rss->as_string;
