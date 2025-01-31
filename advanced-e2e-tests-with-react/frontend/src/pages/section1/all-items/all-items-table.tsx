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

import {
  TableProps,
  StatusIndicator,
  Table,
  PropertyFilter,
  Pagination,
  Box,
  SpaceBetween,
  Button,
} from "@cloudscape-design/components";
import {
  useCollection,
  PropertyFilterProperty,
  PropertyFilterOperator,
} from "@cloudscape-design/collection-hooks";
import RouterLink from "../../../components/wrappers/router-link";
import { useEffect, useState } from "react";
import { TextHelper } from "../../../common/helpers/text-helper";
import { PropertyFilterI18nStrings } from "../../../common/i18n/property-filter-i18n-strings";
import { AllItemsPageHeader } from "./all-items-header";
import { Item } from "../../../common/types";
import { Utils } from "../../../common/utils";
import { useItems } from "../../../context/ItemsContext";

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

const ItemColumnFilteringProperties: PropertyFilterProperty[] = [
  {
    propertyLabel: "Name",
    key: "name",
    groupValuesLabel: "Name values",
    operators: [":", "!:", "=", "!="] as PropertyFilterOperator[],
  },
  {
    propertyLabel: "Type",
    key: "type",
    groupValuesLabel: "Type values",
    operators: [":", "!:", "=", "!="] as PropertyFilterOperator[],
  },
  {
    propertyLabel: "Status",
    key: "status",
    groupValuesLabel: "Status values",
    operators: [":", "!:", "=", "!="] as PropertyFilterOperator[],
  },
  {
    propertyLabel: "Details",
    key: "details",
    groupValuesLabel: "Details",
    defaultOperator: ">" as PropertyFilterOperator,
    operators: ["<", "<=", ">", ">="] as PropertyFilterOperator[],
  },
].sort((a, b) => a.propertyLabel.localeCompare(b.propertyLabel));

export default function AllItemsTable() {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState<Item[]>([]);
  const allItems = useItems();
  const {
    items,
    actions,
    filteredItemsCount,
    collectionProps,
    paginationProps,
    propertyFilterProps,
  } = useCollection(data, {
    propertyFiltering: {
      filteringProperties: ItemColumnFilteringProperties,
      empty: (
        <Box margin={{ vertical: "xs" }} textAlign="center" color="inherit">
          <div>
            <b>No Items</b>
            <Box variant="p" color="inherit">
              No items associated with this resource.
            </Box>
          </div>
        </Box>
      ),
      noMatch: (
        <Box margin={{ vertical: "xs" }} textAlign="center" color="inherit">
          <SpaceBetween size="xxs">
            <div>
              <b>No matches</b>
              <Box variant="p" color="inherit">
                We can't find a match.
              </Box>
            </div>
            <Button
              onClick={() =>
                actions.setPropertyFiltering({ tokens: [], operation: "and" })
              }
            >
              Clear filter
            </Button>
          </SpaceBetween>
        </Box>
      ),
    },
    pagination: { pageSize: 25 },
    sorting: {
      defaultState: {
        sortingColumn: ItemsColumnDefinitions[0],
        isDescending: true,
      },
    },
    selection: {},
  });

  useEffect(() => {
    (async () => {
      await Utils.promiseSetTimeout(100);
      setData(allItems);
      setLoading(false);
    })();
  }, []);

  return (
    <Table
      {...collectionProps}
      items={items}
      columnDefinitions={ItemsColumnDefinitions}
      selectionType="single"
      variant="full-page"
      stickyHeader={true}
      resizableColumns={true}
      header={
        <AllItemsPageHeader
          selectedItems={collectionProps.selectedItems ?? []}
          counter={
            loading
              ? undefined
              : TextHelper.getHeaderCounterText(
                  data,
                  collectionProps.selectedItems
                )
          }
        />
      }
      loading={loading}
      loadingText="Loading Items"
      filter={
        <PropertyFilter
          {...propertyFilterProps}
          i18nStrings={PropertyFilterI18nStrings}
          filteringPlaceholder={"Filter Items"}
          countText={TextHelper.getTextFilterCounterText(filteredItemsCount)}
          expandToViewport={true}
        />
      }
      pagination={<Pagination {...paginationProps} />}
    />
  );
}
