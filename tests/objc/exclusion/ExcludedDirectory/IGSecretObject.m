//
//  IGSecretObject.m
//
//  Created by Pierre Dulac on 09/10/2015.
//

#import "IGSecretObject.h"

@interface IGSecretObject ()

@property (nonatomic, strong, readwrite) NSString *secret;

@end

@implementation IGSecretObject

- (void)configureSecret {
    self.secret = NSLocalizedString(@"Should be excluded from localization", @"secret message (or not)");
}

@end
