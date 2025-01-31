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

import { createContext, ReactNode, useContext, useReducer } from 'react';
import { itemsReducer } from '../common/reducers/itemsReducer';
import { ApiClient } from '../common/api-client/api-client';
import { Item } from '../common/types';

const ItemsContext = createContext<Item[] | null>(null);
const ItemsDispatchContext = createContext<React.Dispatch<any> | null>(null);

interface ItemsProviderProps {
    children: ReactNode;
  }

export function ItemsProvider({ children }: ItemsProviderProps) {
  const [items, dispatch] = useReducer(itemsReducer, fetchTasks());

  return (
    <ItemsContext.Provider value={items}>
      <ItemsDispatchContext.Provider
        value={dispatch}
      >
        {children}
      </ItemsDispatchContext.Provider>
    </ItemsContext.Provider>
  );
}

export function useItems() {
    const context = useContext(ItemsContext);
    if (context === null) throw new Error('useItems must be used within an ItemsProvider');
    return context;
  }
  
  export function useItemsDispatch() {
    const context = useContext(ItemsDispatchContext);
    if (context === null) throw new Error('useItemsDispatch must be used within an ItemsProvider');
    return context;
  }


function fetchTasks() {
    const apiClient = new ApiClient();
    const data = apiClient.items.getItems();
    return data;
}
