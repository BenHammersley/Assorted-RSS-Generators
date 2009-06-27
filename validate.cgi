#!/usr/bin/perl -w
# RSS generator from w3 validator results

use strict;
use XML::RSS;
use CGI qw(:standard);
use LWP::Simple 'get';
use XML::Simple;


my $cgi = CGI::new();
my $url = $cgi->param('url');

my $validator_results_in_xml = get("http://validator.w3.org/check?uri=$url;output=xml");

# This split is to trim off the top of the XML the validator produces, because XML::Simple throws an error with it.

my ($broken_xml_to_ignore, $trimmed_validator_results_in_xml) = split(/]>/, $validator_results_in_xml);


my $parsed_validator_results = XMLin($trimmed_validator_results_in_xml);

my $rss = new XML::RSS(version => '0.91');

$rss -> channel(title => "XHTML Validation results for $url");
$rss -> channel(link => "http://validator.w3.org/check?uri=$url");


foreach my $error (@{$parsed_validator_results->{'messages'}->{'msg'}}) {
    $rss -> add_item(
        title => "Line $error->{'line'} $error->{'content'}",
        link => "http://validator.w3.org/check?uri=$url",
        description => "Line $error->{'line'} $error->{'content'}",
        );
}

print header('application/xml+rss');
print $rss->as_string;