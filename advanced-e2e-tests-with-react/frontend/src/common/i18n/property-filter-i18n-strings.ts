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

import { PropertyFilterProps } from "@cloudscape-design/components";

export const PropertyFilterI18nStrings: PropertyFilterProps.I18nStrings = {
  filteringAriaLabel: "your choice",
  dismissAriaLabel: "Dismiss",

  groupValuesText: "Values",
  groupPropertiesText: "Properties",
  operatorsText: "Operators",

  operationAndText: "and",
  operationOrText: "or",

  operatorLessText: "Less than",
  operatorLessOrEqualText: "Less than or equal",
  operatorGreaterText: "Greater than",
  operatorGreaterOrEqualText: "Greater than or equal",
  operatorContainsText: "Contains",
  operatorDoesNotContainText: "Does not contain",
  operatorEqualsText: "Equals",
  operatorDoesNotEqualText: "Does not equal",

  editTokenHeader: "Edit filter",
  propertyText: "Property",
  operatorText: "Operator",
  valueText: "Value",
  cancelActionText: "Cancel",
  applyActionText: "Apply",
  allPropertiesLabel: "All properties",

  tokenLimitShowMore: "Show more",
  tokenLimitShowFewer: "Show fewer",
  clearFiltersText: "Clear filters",
  removeTokenButtonAriaLabel: (token) =>
    `Remove token ${token.propertyKey} ${token.operator} ${token.value}`,
  enteredTextLabel: (text) => `Use: "${text}"`,
};
