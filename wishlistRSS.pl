#!/usr/bin/perl
=begin lip

=head1 NAME

Amazon.co.uk Wishlist to RSS

=head1 SYNOPSIS

Convert an Amazon.co.uk Wishlist to RSS

=head1 DESCRIPTION

My wife loves books, and as a loving and dutiful husband,, her Amazon wishlist is required reading for Christmas, Birthdays, and all other occasions. But keeping track of the wishlist is a pain if I have to trudge over to Amazon everytime. Far better to have my feed reader do it for me, with the help of a little script.

This uses the Amazon Web Services API to do its evil work. This can be either REST or SOAP based, so you can choose your own preferred poison. For fun, I'll do this using the REST interface, and then use XPath to parse the resultant XML. My idea of fun might not be the same as yours.

=head1 AUTHOR

Ben Hammersley <ben@benhammersley.com>

=head1 BUGS

=head1 SEE ALSO

=head1 COPYRIGHT

=cut

########### CODE BEGINS ##########

=item

So, like always, we fire up the script with the loading of the modules and setting of some global variables. The obligatory <code>use strict;</code> and <code>use warnings;</code>, and the required Amazon API subscription key. You'll need to get your own, from 

=cut

use strict;
use warnings;
use XML::RSS;
use XML::XPath;
use XML::XPath::XMLParser;
use LWP::Simple;

my $amazon_subscription_id = "08R1SHPFGCA8VYT9P802";
my $list_id = "3DC9C0E48Z5C6";

=item

The URL query to request the wishlist is this:

http://webservices.amazon.co.uk/onca/xml?Service=AWSProductData&SubscriptionId=08R1SHPFGCA8VYT9P802&Operation=ListLookup&ProductPage=15&ListType=WishList&ListId=3DC9C0E48Z5C6&ResponseGroup=Request,ListItems

So, let's snaffle the data using LWP::Simple

=cut

my $query_url = "http://webservices.amazon.co.uk/onca/xml?Service=AWSProductData&SubscriptionId=$amazon_subscription_id&Operation=ListLookup&ProductPage=15&ListType=WishList&ListId=$list_id&ResponseGroup=Request,ListItems";

print "$query_url";

my $wishlist_in_xml = get("$query_url");

=item

And place it into the Parser

=cut

my $parser = XML::XPath->new(xml => "$wishlist_in_xml") or die("Could not parse file");

my $nodeset = $parser->find('/ListLookupResponse/Lists/List[1]/ListItem');
    
foreach my $item ($nodeset->get_nodelist) {
        
        my $item_xml = XML::XPath::XMLParser::as_string($item);
        print "FOUND\n\n", XML::XPath::XMLParser::as_string($item),"\n\n";

    }



##################################

=end lip

=cut
