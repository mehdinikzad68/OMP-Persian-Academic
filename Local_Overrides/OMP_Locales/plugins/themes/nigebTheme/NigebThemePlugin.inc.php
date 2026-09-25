<?php

/**
 * @file NigebThemePlugin.inc.php
 *
 * Copyright (c) 2024 Nigeb
 * Distributed under the GNU GPL v3. For full terms see the file docs/COPYING.
 *
 * @class NigebThemePlugin
 *
 * @ingroup plugins_themes_nigebTheme
 *
 * @brief Nigeb theme plugin for OMP 3.5.
 */

use PKP\plugins\ThemePlugin;

class NigebThemePlugin extends ThemePlugin {

    /**
     * @copydoc ThemePlugin::init()
     */
    public function init() {

        // Inherit all foundational styles, grid, and layout from the OMP Default Theme.
        // Without this, OMP renders unstyled HTML because the core CSS is never loaded.
        $this->setParent('defaultthemeplugin');

        // (a) Load the main components stylesheet (LESS → auto-compiled to CSS)
        $this->addStyle('components', 'styles/OMP-Theme-Components.less');

        // (b) Load the Vazirmatn font from Google Fonts.
        //
        // IMPORTANT NOTE ON THE API:
        // ThemePlugin::addStyle() signature is:
        //     addStyle(string $name, string $style, array $args = [])
        //
        // The second parameter ($style) must be a STRING, NOT an array.
        // Passing an array like ['url' => '...'] is NOT supported — there is no
        // such signature in the OMP 3.5 ThemePlugin source.
        //
        // For external URLs, we use the 'baseUrl' argument set to an empty string
        // so that addStyle() does not prepend the plugin's local base path.
        // From the source (ThemePlugin.php, addStyle method):
        //   if (isset($args['baseUrl'])) {
        //       $args['style'] = $args['baseUrl'] . $style;
        //   }
        // Setting 'baseUrl' => '' makes the full external URL pass through as-is.
        $this->addStyle(
            'vazirmatn-font',
            'https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap',
            ['baseUrl' => '']
        );
    }

    /**
     * @copydoc Plugin::getDisplayName()
     */
    public function getDisplayName() {
        return 'Nigeb Theme';
    }

    /**
     * @copydoc Plugin::getDescription()
     */
    public function getDescription() {
        return 'A custom theme for OMP developed by Nigeb.';
    }
}
