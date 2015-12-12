//
//  IGSimpleObject.m
//
//  Created by Pierre Dulac on 09/10/2015.
//

#import "IGSimpleObject.h"

@interface IGSimpleObject ()

@property (nonatomic, strong, readwrite) NSString *title;
@property (nonatomic, strong, readwrite) NSString *subtitle;

@end

@implementation IGSimpleObject

- (void)configureWithName:(NSString *)name {
    self.title = [NSString stringWithFormat:NSLocalizedString(@"Hi %@ !", @"title for the simple object"), name];
    self.subtitle = NSLocalizedString(@"How are you doing today", @"subtitle for the simple object");
}

@end
