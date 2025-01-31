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

import { Item } from "../types";

export class ItemsApiClient {
  getItems(): Item[]{
    const items: Item[] = []; 
    for (let i = 0; i < 150; i++) {
      items.push({
        itemId: i.toString(),
        name: `Item ${i}`,
        type: `Type ${i}`,
        status: i % 10 === 0 ? "warning" : i % 15 === 1 ? "error" : "success",
        details: i * 10,
      });
    }
    return items;
  }
  
  createItem( id: number, item: Item,): Item {
    return {
      itemId: id.toString(),
      name: item.name,
      type: `Type ${id}`,
      status: id % 10 === 0 ? "warning" : id % 15 === 1 ? "error" : "success",
      details: id * 10,
    }
  }
}