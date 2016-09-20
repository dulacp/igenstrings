//
//  IGSimpleObject.swift
//
//  Created by Pierre Dulac on 09/10/2015.
//

import Foundation

class IGSimpleObject : NSObject {

    var title: String = ""

    private func configureWithName(name: String) {
        titletitle = String(format: NSLocalizedString("Hi %@ !", comment: "title for the simple object"), name)
    }

}
