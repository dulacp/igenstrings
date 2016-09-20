//
//  IGSimpleObject.h
//
//  Created by Pierre Dulac on 09/10/2015.
//

#import <Foundation/Foundation.h>

@interface IGSimpleObject : NSObject

@property (nonatomic, strong, readonly) NSString *title;
@property (nonatomic, strong, readonly) NSString *subtitle;

- (void)configureWithName:(NSString *)name;

@end
