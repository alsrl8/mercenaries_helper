def read_wiki_sources(wiki_source_filename, data_filename):
    print('Scraping wiki page sources')
    mercenary_names = []
    with open(wiki_source_filename, 'r') as wiki:
        while True:
            s = wiki.readline()
            if not s:
                print(f'Finished scraping wiki page sources. number of cards: {len(mercenary_names)}')
                with open(data_filename, 'w') as w_data:
                    for name in mercenary_names:
                        w_data.write(name + '\n')
                break
            else:
                i = s.find('alt=')
                if i == -1:
                    continue
                j = s.find('"', i + len('alt="'))
                name = s[i + 5:j]
                name = name.replace('&#39;', '\'')  # fix apostrophe correctly
                mercenary_names.append(name)
