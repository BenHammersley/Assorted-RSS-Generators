#!/usr/bin/perl
=begin lip

=head1 NAME

Last Modified Files

=head1 DESCRIPTION

There are lots of reasons to have an ever-updating list of recently modified files. Security, for one, but it's also a useful system for helping you group working files in your mind. I'm forever loosing track of files I'm working on &mdash; especially overnight &mdash; and this feed helps a great deal. For collaborative working it's a godsend, as you can see what other activity is going on automatically. I also have one of these pointed at a shared directory where friends drop music and silly mpegs. Altogether, for something so simple, it's remarkably useful.

It's a CGI script, taking a single parameter <literal>path</literal>, which should be equal to the absolute path on your file system that you wish to look below. For example, <literal>http://www.example.org/lastmodified.cgi?path=/users/ben</literal>

=cut

=item
Once again into the <literal>warnings</literal> and the <literal>strict</literal>, <literal>XML::RSS</literal> and <literal>CGI</literal> of course, plus <literal>Date::Manip</literal> for the dateline and <literal>File::Find</literal> for its directory traversing capabilities. Lovely. All set? Good.

=cut

use warnings;
use strict;
use XML::RSS;
use CGI qw(:standard);
use File::Find;
use Date::Manip;
use diagnostics;

=item

By now you should be getting the hang of this. We're firing up the CGI module, and snaffling the parameter we are passing to it, then setting up the feed. No great mystery here, in other words. Really, this is somewhat the point: feeds are very simple things. It's the ideas of how to use them that are valuable.

=cut

my $cgi             = CGI::new();
my $start_directory = $cgi->param('path');

my $rss = new XML::RSS(version => '2.0');
$rss -> channel(title => "Last modified from $start_directory",
				link => "file:/$start_directory",
				description => "A list of all of the files in $start_directory, with their modification dates added in");

=item

Here's the real meat of the script. We're using the <literal>find</literal> function from the <literal>File::Find</literal> module, to traverse the directory we've given it, and throw all of the file data into an array.

=cut

find (\&search_and_rss, $start_directory);

sub search_and_rss {
    
    my $last_modified_date = (stat($File::Find::name)) [9];
    my $parsed_date = &ParseDate("epoch $last_modified_date");
    my $pubDate = &UnixDate($parsed_date, "%g");
   
    print "$pubDate";
   
    $rss -> add_item(title => "$File::Find::name",
                     link => "file:\/\/$File::Find::name",
                     description => "$File::Find::name",
                     pubDate => "$pubDate",
                     );
                                
}

print header('application/xml');
print $rss->as_string;

=end lip

=cut
