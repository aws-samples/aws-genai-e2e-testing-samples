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

import { useEffect, useState } from "react";
import {
  Box,
  SpaceBetween,
  TableProps,
  Header,
  Table,
  StatusIndicator,
} from "@cloudscape-design/components";
import RouterButton from "../../components/wrappers/router-button";
import RouterLink from "../../components/wrappers/router-link";
import { TextHelper } from "../../common/helpers/text-helper";
import { Item } from "../../common/types";
import { useItems } from "../../context/ItemsContext";
import { Utils } from "../../common/utils";

const ItemsColumnDefinitions: TableProps.ColumnDefinition<Item>[] = [
  {
    id: "name",
    header: "Name",
    sortingField: "name",
    cell: (item) => (
      <RouterLink href={`/section1/items/${item.itemId}`}>
        {item.name}
      </RouterLink>
    ),
    isRowHeader: true,
  },
  {
    id: "type",
    header: "Type",
    sortingField: "type",
    cell: (item) => item.type,
  },
  {
    id: "status",
    header: "Status",
    sortingField: "status",
    cell: (item) => (
      <StatusIndicator type={item.status}>{item.status}</StatusIndicator>
    ),
    minWidth: 120,
  },
  {
    id: "details",
    header: "Details",
    sortingField: "details",
    cell: (item) => item.details,
  },
];

export default function ItemsTable() {
  const [loading, setLoading] = useState(true);
  const [items, setItems] = useState<Item[]>([]);
  const [selectedItems, setSelectedItems] = useState<Item[]>([]);
  const allItems = useItems();

  useEffect(() => {
    (async () => {
      await Utils.promiseSetTimeout(100);
      setItems(allItems);
      setLoading(false);
    })();
  }, []);

  return (
    <Table
      loading={loading}
      loadingText="Loading Items"
      selectionType="single"
      empty={
        <Box margin={{ vertical: "xs" }} textAlign="center" color="inherit">
          <SpaceBetween size="xxs">
            <div>
              <b>No Items</b>
              <Box variant="p" color="inherit">
                Item is a thing that is used to do something.
              </Box>
            </div>
            <RouterButton href="/section1/add">Add Item</RouterButton>
          </SpaceBetween>
        </Box>
      }
      columnDefinitions={ItemsColumnDefinitions}
      items={items.slice(0, 5)}
      selectedItems={selectedItems}
      onSelectionChange={(event: {
        detail: TableProps.SelectionChangeDetail<Item>;
      }) => setSelectedItems(event.detail.selectedItems)}
      header={
        <Header
          counter={
            !loading
              ? TextHelper.getHeaderCounterText(items, selectedItems)
              : undefined
          }
          actions={
            <SpaceBetween direction="horizontal" size="xs">
              <RouterButton
                disabled={selectedItems.length !== 1}
                href={`/section1/items/${
                  selectedItems.length > 0 ? selectedItems[0].itemId : ""
                }`}
              >
                View
              </RouterButton>
              <RouterButton href="/section1/add">Add Item</RouterButton>
            </SpaceBetween>
          }
        >
          Items
        </Header>
      }
      footer={
        <Box textAlign="center">
          <RouterLink href="/section1">View all Items</RouterLink>
        </Box>
      }
    />
  );
}
