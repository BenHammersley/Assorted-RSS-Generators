#!/usr/bin/perl

=begin lip

=head1 NAME

Installed Perl Modules

=head1 DESCRIPTION

Another interesting use of a Feed is to keep track of changing system configurations. This is a simple example. I have two machines running my scripts, one is my laptop and the other a server in a rack somewhere in North America.

=cut

use warnings;
use strict;
use CGI qw(:standard);
use XML::RSS;
use ExtUtils::Installed;

my $installed    = ExtUtils::Installed->new();
my $machine_name = `uname -n`;

my $rss = new XML::RSS( version => '2.0' );
$rss->channel(
    title       => "Perl Modules on $machine_name",
    link        => "http://www.benhammersley.com/tools/",
    description => "A list of installed Perl modules on $machine_name"
);

foreach my $module ( $installed->modules() ) {
    my $version = $installed->version($module) || "???";

    $rss->add_item(
        title       => "$module $version",
        description => "$module $version",
        link        => "http://search.cpan.org/search%3fmodule=$module",
    );
}

print header('application/rss+xml');
print $rss->as_string;

=end lip

=cut

