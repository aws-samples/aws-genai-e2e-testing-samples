/*
 * Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: MIT-0
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this
 * software and associated documentation files (the "Software"), to deal in the Software
 * without restriction, including without limitation the rights to use, copy, modify,
 * merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 * INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
 * PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 * OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

import { ApiClient } from "../api-client/api-client";
import { Item } from "../types";

type ReducerAction = {
    type: 'CREATE' | 'LIST';
    payload: Item
}

export function itemsReducer(items: Item[], action: ReducerAction) {
    const apiClient = new ApiClient();
    try {
        switch (action.type) {
            case 'CREATE': {
                const newItem = apiClient.items.createItem(items.length, action.payload);
                console.log('newItem', newItem)
                return [...items, newItem];
            }
            case 'LIST':
                return items;
            default:
                throw new Error(`Unknown action: ${action.type}`);
        }
    } catch (error) {
        console.error('Error in itemsReducer:', error);
        throw error instanceof Error 
            ? error 
            : new Error('An unknown error occurred');
    }
}
