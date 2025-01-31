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

import { Mode, applyMode } from "@cloudscape-design/global-styles";
import { NavigationPanelState } from "../types";

const PREFIX = "example-app";
const THEME_STORAGE_NAME = `${PREFIX}-theme`;
const NAVIGATION_PANEL_STATE_STORAGE_NAME = `${PREFIX}-navigation-panel-state`;

export abstract class StorageHelper {
  static getTheme() {
    const value = localStorage.getItem(THEME_STORAGE_NAME) ?? Mode.Light;
    const theme = value === Mode.Dark ? Mode.Dark : Mode.Light;

    return theme;
  }

  static applyTheme(theme: Mode) {
    localStorage.setItem(THEME_STORAGE_NAME, theme);
    applyMode(theme);

    document.documentElement.style.setProperty(
      "--app-color-scheme",
      theme === Mode.Dark ? "dark" : "light"
    );

    return theme;
  }

  static getNavigationPanelState(): NavigationPanelState {
    const value =
      localStorage.getItem(NAVIGATION_PANEL_STATE_STORAGE_NAME) ??
      JSON.stringify({
        collapsed: true,
      });

    let state: NavigationPanelState | null = null;
    try {
      state = JSON.parse(value);
    } catch {
      state = {};
    }

    return state ?? {};
  }

  static setNavigationPanelState(state: Partial<NavigationPanelState>) {
    const currentState = this.getNavigationPanelState();
    const newState = { ...currentState, ...state };
    const stateStr = JSON.stringify(newState);
    localStorage.setItem(NAVIGATION_PANEL_STATE_STORAGE_NAME, stateStr);

    return newState;
  }
}
