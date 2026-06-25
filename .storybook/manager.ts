import { addons } from 'storybook/manager-api';

const ADDON_ID = 'hide-story';
const STORAGE_KEY = 'storybook-hidden';
const CHANNEL_EVENT = 'hide-story/visibility-changed';

addons.register(ADDON_ID, (api) => {
  function getHidden(): Set<string> {
    try {
      return new Set(JSON.parse(localStorage.getItem(STORAGE_KEY) ?? '[]'));
    } catch {
      return new Set();
    }
  }

  function applyFilter() {
    const hidden = getHidden();
    api.experimental_setFilter(ADDON_ID, (item) => !hidden.has(item.id));
  }

  applyFilter();

  const channel = api.getChannel();
  channel.on(CHANNEL_EVENT, applyFilter);
});
