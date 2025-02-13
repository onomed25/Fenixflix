def canais_list(server):
    canais = [
    {
        "id": "skyflix:globosp",
        "type": "tv",
        "name": "Globo SP",
        "poster": f"{server}https://embehub.com/img/globo.png",
        "background": f"{server}https://embehub.com/img/globo.png",
        "description": "Canal Globo SP ao vivo.",
        "genres": ["Canais Abertos"],
        "streams": [
            {
                "url": "https://embedcanaistv.site/globosp/video.m3u8",
                "title": "Globo SP",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://embedcanaistv.com",
                            "Referer": "https://embedcanaistv.com/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:globonordeste",
        "server": "redecanais",
        "page": "https://redecanaistv.ps/link/stream.m3u8?categoria=fhd&canal=c0hIM0JOcmVXRnNkRkRoRDJseHI3aWpaZzloZ0Z6UT0=",
        "type": "tv",
        "name": "Globo Nordeste",
        "poster": f"{server}https://embehub.com/img/globo.png",
        "background": f"{server}https://embehub.com/img/globo.png",
        "description": "Canal Globo Nordeste ao vivo.",
        "genres": ["Canais Abertos"],
        "streams": [
            {
                "url": "https://play.embehub.com/GLOBO_NORDESTE/index.fmp4.m3u8",
                "title": "Globo Nordeste",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://redecanaistv.ps",
                            "Referer": "https://redecanaistv.ps/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:sbtsp",
        "server": "redecanais",
        "page": "https://redecanaistv.ps/link/stream.m3u8?categoria=fhd&canal=c0hIM0JOclpVbEFlRmpoUzEwbz0=",
        "type": "tv",
        "name": "SBT SP",
        "poster": f"{server}https://embehub.com/img/thumb-sbt.jpg",
        "background": f"{server}https://embehub.com/img/thumb-sbt.jpg",
        "description": "Canal SBT ao vivo.",
        "genres": ["Canais Abertos"],
        "streams": [
            {
                "url": "https://embedcanaistv.site/sbtsp/video.m3u8",
                "title": "SBT SP",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://redecanaistv.ps",
                            "Referer": "https://redecanaistv.ps/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:bandsp",
        "server": "redecanais",
        "page": "https://redecanaistv.ps/link/stream.m3u8?categoria=fhd&canal=c0hIM0JOclpWbFFhRURoRDFGQmc=",        
        "type": "tv",
        "name": "BAND SP",
        "poster": f"{server}https://embehub.com/img/thumb-band.jpg",
        "background": f"{server}https://embehub.com/img/thumb-band.jpg",
        "description": "Canal BAND ao vivo.",
        "genres": ["Canais Abertos"],
        "streams": [
            {
                "url": "https://embedcanaistv.site/bandsp/video.m3u8",
                "title": "BAND SP",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://redecanaistv.ps",
                            "Referer": "https://redecanaistv.ps/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:redetv",
        "server": "redecanais",
        "page": "https://redecanaistv.ps/link/stream.m3u8?categoria=fhd&canal=c0hIM0JOclpWbFFhRURoRDFGQmc=",        
        "type": "tv",
        "name": "REDE TV",
        "poster": f"{server}https://embehub.com/img/thumb-redetv.jpg",
        "background": f"{server}https://embehub.com/img/thumb-redetv.jpg",
        "description": "Canal REDE TV ao vivo.",
        "genres": ["Canais Abertos"],
        "streams": [
            {
                "url": "https://embedcanaistv.site/redetv/video.m3u8",
                "title": "REDE TV",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://redecanaistv.ps",
                            "Referer": "https://redecanaistv.ps/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:tvbrasil",
        "type": "tv",
        "name": "TV BRASIL",
        "poster": f"{server}https://embehub.com/img/thumb-tvbrasil.jpg",
        "background": f"{server}https://embehub.com/img/thumb-tvbrasil.jpg",
        "description": "Canal TV BRASIL ao vivo.",
        "genres": ["Canais Abertos"],
        "streams": [
            {
                "url": "https://play.embehub.com/TVBRASIL/index.fmp4.m3u8",
                "title": "TV BRASIL",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/TVBRASIL/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:futura",
        "type": "tv",
        "name": "FUTURA",
        "poster": f"{server}https://embehub.com/img/thumb-futura.png",
        "background": f"{server}https://embehub.com/img/thumb-futura.png",
        "description": "Canal FUTURA ao vivo.",
        "genres": ["Canais Abertos"],
        "streams": [
            {
                "url": "https://play.embehub.com/FUTURA/index.fmp4.m3u8",
                "title": "FUTURA",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/FUTURA/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:recordsp",
        "type": "tv",
        "name": "RECORD SP",
        "poster": f"{server}https://embehub.com/img/thumb-record.jpg",
        "background": f"{server}https://embehub.com/img/thumb-record.jpg",
        "description": "Canal RECORD SP ao vivo.",
        "genres": ["Canais Abertos"],
        "streams": [
            {
                "url": "https://embedcanaistv.site/recordsp/video.m3u8",
                "title": "RECORD SP",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://embedcanaistv.com",
                            "Referer": "https://embedcanaistv.com/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:viva",
        "type": "tv",
        "name": "VIVA",
        "poster": f"{server}https://embehub.com/img/thumb-viva.jpg",
        "background": f"{server}https://embehub.com/img/thumb-viva.jpg",
        "description": "Canal VIVA ao vivo.",
        "genres": ["Variedades"],
        "streams": [
            {
                "url": "https://anonstream.zip/viva/index.m3u8",
                "title": "VIVA",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://embedstream.org",
                            "Referer": "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:bis",
        "type": "tv",
        "name": "BIS",
        "poster": f"{server}https://embehub.com/img/biz.png",
        "background": f"{server}https://embehub.com/img/biz.png",
        "description": "Canal BIS ao vivo.",
        "genres": ["Variedades"],
        "streams": [
            {
                "url": "https://anonstream.zip/bis/index.m3u8",
                "title": "BIS",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://embedstream.org",
                            "Referer": "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:gnt",
        "type": "tv",
        "name": "GNT",
        "poster": f"{server}https://embehub.com/img/gnt.jpg",
        "background": f"{server}https://embehub.com/img/gnt.jpg",
        "description": "Canal GNT ao vivo.",
        "genres": ["Variedades"],
        "streams": [
            {
                "url": "https://anonstream.zip/gnt/index.m3u8",
                "title": "GNT",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://embedstream.org",
                            "Referer": "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:multishow",
        "type": "tv",
        "name": "MULTISHOW",
        "poster": f"{server}https://embehub.com/img/multishow.png",
        "background": f"{server}https://embehub.com/img/multishow.png",
        "description": "Canal MULTISHOW ao vivo.",
        "genres": ["Variedades"],
        "streams": [
            {
                "url": "https://anonstream.zip/multishow/index.m3u8",
                "title": "MULTISHOW",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://embedstream.org",
                            "Referer": "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:off",
        "type": "tv",
        "name": "CANAL OFF",
        "poster": f"{server}https://embehub.com/img/canaloff.webp",
        "background": f"{server}https://embehub.com/img/canaloff.webp",
        "description": "Canal OFF ao vivo.",
        "genres": ["Variedades"],
        "streams": [
            {
                "url": "https://play.embehub.com/CANAL_OFF/index.fmp4.m3u8",
                "title": "CANAL OFF",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/CANAL_OFF/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:adultswim",
        "type": "tv",
        "name": "ADULT SWIM",
        "poster": f"{server}https://embehub.com/img/thumb-adultswim.jpg",
        "background": f"{server}https://embehub.com/img/thumb-adultswim.jpg",
        "description": "Canal ADULT SWIM ao vivo.",
        "genres": ["Variedades"],
        "streams": [
            {
                "url": "https://anonstream.zip/adultswim/index.m3u8",
                "title": "MULTISHOW",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://embedstream.org",
                            "Referer": "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:amc",
        "type": "tv",
        "name": "AMC",
        "poster": f"{server}https://embehub.com/img/AMC.jpg",
        "background": f"{server}https://embehub.com/img/AMC.jpg",
        "description": "Canal AMC ao vivo.",
        "genres": ["Filmes e Series"],
        "streams": [
            {
                "url": "https://play.embehub.com/AMC/index.fmp4.m3u8",
                "title": "AMC",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/AMC/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:animalplanet",
        "type": "tv",
        "name": "ANIMAL PLANET",
        "poster": f"{server}https://embehub.com/img/thumb-animalplanet.jpg",
        "background": f"{server}https://embehub.com/img/thumb-animalplanet.jpg",
        "description": "Canal ANIMAL PLANET ao vivo.",
        "genres": ["Documentarios"],
        "streams": [
            {
                "url": "https://play.embehub.com/ANIMAL_PLANET/index.fmp4.m3u8",
                "title": "ANIMAL PLANET",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/ANIMAL_PLANET/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:arte1",
        "type": "tv",
        "name": "ARTE 1",
        "poster": f"{server}https://embehub.com/img/thumb-arte1.jpg",
        "background": f"{server}https://embehub.com/img/thumb-arte1.jpg",
        "description": "Canal ARTE 1 ao vivo.",
        "genres": ["Filmes e Series"],
        "streams": [
            {
                "url": "https://play.embehub.com/ARTE1/index.fmp4.m3u8",
                "title": "ARTE 1",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/ARTE1/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:axn",
        "type": "tv",
        "name": "AXN",
        "poster": f"{server}https://embehub.com/img/thumb-axn.jpg",
        "background": f"{server}https://embehub.com/img/thumb-axn.jpg",
        "description": "Canal AXN ao vivo.",
        "genres": ["Filmes e Series"],
        "streams": [
            {
                "url": "https://anonstream.zip/axn/index.m3u8",
                "title": "AXN",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://embedstream.org",
                            "Referer": "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:canalbrasil",
        "type": "tv",
        "name": "CANAL BRASIL",
        "poster": f"{server}https://embehub.com/img/thumb-canalbrasil.jpg",
        "background": f"{server}https://embehub.com/img/thumb-canalbrasil.jpg",
        "description": "Canal BRASIL ao vivo.",
        "genres": ["Filmes e Series"],
        "streams": [
            {
                "url": "https://play.embehub.com/CANAL_BRASIL/index.fmp4.m3u8",
                "title": "CANAL BRASIL",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/CANAL_BRASIL/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:discoverychannel",
        "type": "tv",
        "name": "DISCOVERY CHANNEL",
        "poster": f"{server}https://embehub.com/img/thumb-discovery.jpg",
        "background": f"{server}https://embehub.com/img/thumb-discovery.jpg",
        "description": "Canal DISCOVERY CHANNEL ao vivo.",
        "genres": ["Documentarios"],
        "streams": [
            {
                "url": "https://play.embehub.com/DISCOVERY_channel/index.fmp4.m3u8",
                "title": "DISCOVERY CHANNEL",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/DISCOVERY_channel/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:discoveryheh",
        "type": "tv",
        "name": "DISCOVERY HOME & HEALTH",
        "poster": f"{server}https://embehub.com/img/thumb-discoveryhomeihealth.jpg",
        "background": f"{server}https://embehub.com/img/thumb-discoveryhomeihealth.jpg",
        "description": "Canal DISCOVERY HOME & HEALTH ao vivo.",
        "genres": ["Documentarios"],
        "streams": [
            {
                "url": "https://play.embehub.com/DISCOVERY_h&h/index.fmp4.m3u8",
                "title": "DISCOVERY HOME & HEALTH",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/DISCOVERY_h&h/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:discoveryturbo",
        "type": "tv",
        "name": "DISCOVERY TURBO",
        "poster": f"{server}https://embehub.com/img/discoveryturbo.png",
        "background": f"{server}https://embehub.com/img/discoveryturbo.png",
        "description": "Canal DISCOVERY TURBO ao vivo.",
        "genres": ["Documentarios"],
        "streams": [
            {
                "url": "https://play.embehub.com/DISCOVERY_turbo/index.fmp4.m3u8",
                "title": "DISCOVERY TURBO",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/DISCOVERY_turbo/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:discoverytheater",
        "type": "tv",
        "name": "DISCOVERY THEATER",
        "poster": f"{server}https://embehub.com/img/discoverytheather.webp",
        "background": f"{server}https://embehub.com/img/discoverytheather.webp",
        "description": "Canal DISCOVERY THEATER ao vivo.",
        "genres": ["Documentarios"],
        "streams": [
            {
                "url": "https://anonstream.zip/discoverytheater/index.m3u8",
                "title": "DISCOVERY THEATER",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://embedstream.org",
                            "Referer": "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:discoveryworld",
        "type": "tv",
        "name": "DISCOVERY WORLD",
        "poster": f"{server}https://embehub.com/img/discoveryworld.png",
        "background": f"{server}https://embehub.com/img/discoveryworld.png",
        "description": "Canal DISCOVERY WORLD ao vivo.",
        "genres": ["Documentarios"],
        "streams": [
            {
                "url": "https://anonstream.zip/discoveryworld/index.m3u8",
                "title": "DISCOVERY WORLD",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://embedstream.org",
                            "Referer": "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:discoveryscience",
        "type": "tv",
        "name": "DISCOVERY SCIENCE",
        "poster": "https://static.wikia.nocookie.net/logopedia/images/6/63/Discovery_Science_LA_2011.png",
        "background": "https://static.wikia.nocookie.net/logopedia/images/6/63/Discovery_Science_LA_2011.png",
        "description": "canal DISCOVERY SCIENCE ao vivo.",
        "genres": ["Documentarios"],
        "streams": [
            {
                "url": "https://anonstream.zip/discoveryscience/index.m3u8",
                "title": "DISCOVERY SCIENCE",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://embedstream.org",
                            "Referer": "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:fx",
        "type": "tv",
        "name": "FX",
        "poster": f"{server}https://embehub.com/img/thumb-fx.jpg",
        "background": f"{server}https://embehub.com/img/thumb-fx.jpg",
        "description": "Canal FX ao vivo.",
        "genres": ["Filmes e Series"],
        "streams": [
            {
                "url": "https://anonstream.zip/fx/index.m3u8",
                "title": "FX",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://embedstream.org",
                            "Referer": "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:hbo",
        "type": "tv",
        "name": "HBO",
        "poster": f"{server}https://embehub.com/img/thumb-hbo.jpg",
        "background": f"{server}https://embehub.com/img/thumb-hbo.jpg",
        "description": "Canal HBO ao vivo.",
        "genres": ["Filmes e Series"],
        "streams": [
            {
                "url": "https://anonstream.zip/hbo/index.m3u8",
                "title": "HBO",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://embedstream.org",
                            "Referer": "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:hbo2",
        "type": "tv",
        "name": "HBO 2",
        "poster": f"{server}https://embehub.com/img/thumb-hbo2.jpg",
        "background": f"{server}https://embehub.com/img/thumb-hbo2.jpg",
        "description": "Canal HBO 2 ao vivo.",
        "genres": ["Filmes e Series"],
        "streams": [
            {
                "url": "https://anonstream.zip/hbo2/index.m3u8",
                "title": "HBO 2",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://embedstream.org",
                            "Referer": "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:hbofamily",
        "type": "tv",
        "name": "HBO FAMILY",
        "poster": f"{server}https://embehub.com/img/thumb-hbofamily.jpg",
        "background": f"{server}https://embehub.com/img/thumb-hbofamily.jpg",
        "description": "Canal HBO FAMILY ao vivo.",
        "genres": ["Filmes e Series"],
        "streams": [
            {
                "url": "https://anonstream.zip/hbofamily/index.m3u8",
                "title": "HBO FAMILY",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://embedstream.org",
                            "Referer": "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:hboplus",
        "type": "tv",
        "name": "HBO PLUS",
        "poster": f"{server}https://embehub.com/img/thumb-hboplus.jpg",
        "background": f"{server}https://embehub.com/img/thumb-hboplus.jpg",
        "description": "Canal HBO PLUS ao vivo.",
        "genres": ["Filmes e Series"],
        "streams": [
            {
                "url": "https://play.embehub.com/HBOPLUS/index.fmp4.m3u8",
                "title": "HBO PLUS",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/HBOPLUS/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:hboxtreme',
        'type': 'tv',
        'name': 'HBO XTREME',
        'poster': f"{server}https://embehub.com/img/hboextreme.webp",
        'background': f"{server}https://embehub.com/img/hboextreme.webp",
        'description': 'canal HBO XTREME ao vivo.',
        'genres': ['Filmes e Series'],
        'streams': [
            {
                'url': "https://anonstream.zip/hboxtreme/index.m3u8",
                'title': "HBO XTREME",
                'behaviorHints': {
                    'notWebReady': True,
                    'proxyHeaders': {
                        'request': {
                            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            'Origin': "https://embedstream.org",
                            'Referer': "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:hbosignature',
        'type': 'tv',
        'name': 'HBO SIGNATURE',
        'poster': "https://simg.nicepng.com/png/small/233-2333073_hbo-signature-latin-atlansia-hbo-signature-logo-png.png",
        'background': "https://simg.nicepng.com/png/small/233-2333073_hbo-signature-latin-atlansia-hbo-signature-logo-png.png",
        'description': 'canal HBO SIGNATURE ao vivo.',
        'genres': ['Filmes e Series'],
        'streams': [
            {
                'url': "https://anonstream.zip/hbosignature/index.m3u8",
                'title': "HBO SIGNATURE",
                'behaviorHints': {
                    'notWebReady': True,
                    'proxyHeaders': {
                        'request': {
                            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            'Origin': "https://embedstream.org",
                            'Referer': "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:history',
        'type': 'tv',
        'name': 'HISTORY',
        'poster': f"{server}https://embehub.com/img/thumb-history.jpg",
        'background': f"{server}https://embehub.com/img/thumb-history.jpg",
        'description': 'Canal HISTORY ao vivo.',
        'genres': ['Documentarios'],
        'streams': [
            {
                'url': "https://play.embehub.com/HISTORY_CHANEL/index.fmp4.m3u8",
                'title': "HISTORY",
                'behaviorHints': {
                    'notWebReady': True,
                    'proxyHeaders': {
                        'request': {
                            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            'Referer': "https://play.embehub.com/HISTORY_CHANEL/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:history2',
        'type': 'tv',
        'name': 'HISTORY 2',
        'poster': f"{server}https://embehub.com/img/thumb-history2.jpg",
        'background': f"{server}https://embehub.com/img/thumb-history2.jpg",
        'description': 'Canal HISTORY 2 ao vivo.',
        'genres': ['Documentarios'],
        'streams': [
            {
                'url': "https://play.embehub.com/HISTORY2/index.fmp4.m3u8",
                'title': "HISTORY 2",
                'behaviorHints': {
                    'notWebReady': True,
                    'proxyHeaders': {
                        'request': {
                            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            'Referer': "https://play.embehub.com/HISTORY2/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:mtv',
        'type': 'tv',
        'name': 'MTV',
        'poster': f"{server}https://embehub.com/img/thumb-mtv.jpg",
        'background': f"{server}https://embehub.com/img/thumb-mtv.jpg",
        'description': 'Canal MTV ao vivo.',
        'genres': ['Variedades'],
        'streams': [
            {
                'url': "https://play.embehub.com/mtv/index.fmp4.m3u8",
                'title': "MTV",
                'behaviorHints': {
                    'notWebReady': True,
                    'proxyHeaders': {
                        'request': {
                            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            'Referer': "https://play.embehub.com/mtv/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:nationalgeographic',
        'type': 'tv',
        'name': 'NATIONAL GEOGRAPHIC',
        'poster': f"{server}https://embehub.com/img/thumb-natgeo.jpg",
        'background': f"{server}https://embehub.com/img/thumb-natgeo.jpg",
        'description': 'Canal NATIONAL GEOGRAPHIC ao vivo.',
        'genres': ['Documentarios'],
        'streams': [
            {
                'url': "https://play.embehub.com/national_geographic/index.fmp4.m3u8",
                'title': "NATIONAL GEOGRAPHIC",
                'behaviorHints': {
                    'notWebReady': True,
                    'proxyHeaders': {
                        'request': {
                            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            'Referer': "https://play.embehub.com/national_geographic/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:paramountnetwork',
        'type': 'tv',
        'name': 'PARAMOUNT NETWORK',
        'poster': f"{server}https://embehub.com/img/thumb-paramount.jpg",
        'background': f"{server}https://embehub.com/img/thumb-paramount.jpg",
        'description': 'Canal PARAMOUNT NETWORK ao vivo.',
        'genres': ['Filmes e Series'],
        'streams': [
            {
                'url': "https://play.embehub.com/PARAMOUNT/index.fmp4.m3u8",
                'title': "PARAMOUNT NETWORK",
                'behaviorHints': {
                    'notWebReady': True,
                    'proxyHeaders': {
                        'request': {
                            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            'Referer': "https://play.embehub.com/PARAMOUNT/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:space',
        'type': 'tv',
        'name': 'SPACE',
        'poster': f"{server}https://embehub.com/img/thumb-space.jpg",
        'background': f"{server}https://embehub.com/img/thumb-space.jpg",
        'description': 'Canal SPACE ao vivo.',
        'genres': ['Filmes e Series'],
        'streams': [
            {
                'url': "https://play.embehub.com/space/index.fmp4.m3u8",
                'title': "SPACE",
                'behaviorHints': {
                    'notWebReady': True,
                    'proxyHeaders': {
                        'request': {
                            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            'Referer': "https://play.embehub.com/space/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:tnt',
        'type': 'tv',
        'name': 'TNT',
        'poster': f"{server}https://embehub.com/img/thumb-tnt.jpg",
        'background': f"{server}https://embehub.com/img/thumb-tnt.jpg",
        'description': 'Canal TNT ao vivo.',
        'genres': ['Filmes e Series'],
        'streams': [
            {
                'url': "https://super-cdn.link/tnt/index.m3u8",
                'title': "TNT",
                'behaviorHints': {
                    'notWebReady': True,
                    'proxyHeaders': {
                        'request': {
                            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            'Origin': "https://embedstream.org",
                            'Referer': "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:telecineaction',
        'type': 'tv',
        'name': 'TELECINE ACTION',
        'poster': f"{server}https://embehub.com/img/thumb-telecineaction.jpg",
        'background': f"{server}https://embehub.com/img/thumb-telecineaction.jpg",
        'description': 'Canal TELECINE ACTION ao vivo.',
        'genres': ['Filmes e Series'],
        'streams': [
            {
                'url': "https://super-cdn.link/telecineaction/index.m3u8",
                'title': "TELECINE ACTION",
                'behaviorHints': {
                    'notWebReady': True,
                    'proxyHeaders': {
                        'request': {
                            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            'Origin': "https://embedstream.org",
                            'Referer': "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:telecinecult',
        'type': 'tv',
        'name': 'TELECINE CULT',
        'poster': f"{server}https://embehub.com/img/thumb-telecinecult.jpg",
        'background': f"{server}https://embehub.com/img/thumb-telecinecult.jpg",
        'description': 'Canal TELECINE CULT ao vivo.',
        'genres': ['Filmes e Series'],
        'streams': [
            {
                'url': "https://super-cdn.link/telecinecult/index.m3u8",
                'title': "TELECINE CULT",
                'behaviorHints': {
                    'notWebReady': True,
                    'proxyHeaders': {
                        'request': {
                            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            'Origin': "https://embedstream.org",
                            'Referer': "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:telecinefun',
        'type': 'tv',
        'name': 'TELECINE FUN',
        'poster': f"{server}https://embehub.com/img/thumb-telecinefun.jpg",
        'background': f"{server}https://embehub.com/img/thumb-telecinefun.jpg",
        'description': 'Canal TELECINE FUN ao vivo.',
        'genres': ['Filmes e Series'],
        'streams': [
            {
                'url': "https://super-cdn.link/telecinefun/index.m3u8",
                'title': "TELECINE FUN",
                'behaviorHints': {
                    'notWebReady': True,
                    'proxyHeaders': {
                        'request': {
                            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            'Origin': "https://embedstream.org",
                            'Referer': "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:telecinepipoca',
        'type': 'tv',
        'name': 'TELECINE PIPOCA',
        'poster': f"{server}https://embehub.com/img/thumb-telecinepipoca.jpg",
        'background': f"{server}https://embehub.com/img/thumb-telecinepipoca.jpg",
        'description': 'Canal TELECINE PIPOCA ao vivo.',
        'genres': ['Filmes e Series'],
        'streams': [
            {
                'url': "https://super-cdn.link/telecinepipoca/index.m3u8",
                'title': "TELECINE PIPOCA",
                'behaviorHints': {
                    'notWebReady': True,
                    'proxyHeaders': {
                        'request': {
                            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            'Origin': "https://embedstream.org",
                            'Referer': "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:telecinepremium',
        'type': 'tv',
        'name': 'TELECINE PREMIUM',
        'poster': f"{server}https://embehub.com/img/thumb-telecinepremium.jpg",
        'background': f"{server}https://embehub.com/img/thumb-telecinepremium.jpg",
        'description': 'Canal TELECINE PREMIUM ao vivo.',
        'genres': ['Filmes e Series'],
        'streams': [
            {
                'url': "https://super-cdn.link/telecinepremium/index.m3u8",
                'title': "TELECINE PREMIUM",
                'behaviorHints': {
                    'notWebReady': True,
                    'proxyHeaders': {
                        'request': {
                            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            'Origin': "https://embedstream.org",
                            'Referer': "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:telecinetouch',
        'type': 'tv',
        'name': 'TELECINE TOUCH',
        'poster': f"{server}https://embehub.com/img/thumb-telecinetouch.jpg",
        'background': f"{server}https://embehub.com/img/thumb-telecinetouch.jpg",
        'description': 'Canal TELECINE TOUCH ao vivo.',
        'genres': ['Filmes e Series'],
        'streams': [
            {
                'url': "https://super-cdn.link/telecinetouch/index.m3u8",
                'title': "TELECINE TOUCH",
                'behaviorHints': {
                    'notWebReady': True,
                    'proxyHeaders': {
                        'request': {
                            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            'Origin': "https://embedstream.org",
                            'Referer': "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:universal',
        'type': 'tv',
        'name': 'UNIVERSAL TV',
        'poster': f"{server}https://embehub.com/img/thumb-universal.jpg",
        'background': f"{server}https://embehub.com/img/thumb-universal.jpg",
        'description': 'Canal UNIVERSAL ao vivo.',
        'genres': ['Filmes e Series'],
        'streams': [
            {
                'url': "https://anonstream.zip/universaltv/index.m3u8",
                'title': "UNIVERSAL TV",
                'behaviorHints': {
                    'notWebReady': True,
                    'proxyHeaders': {
                        'request': {
                            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            'Origin': "https://embedstream.org",
                            'Referer': "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:syfy',
        'type': 'tv',
        'name': 'SYFY',
        'poster': f"{server}https://embehub.com/img/syfy.jpg",
        'background': f"{server}https://embehub.com/img/syfy.jpg",
        'description': 'Canal SYFY ao vivo.',
        'genres': ['Filmes e Series'],
        'streams': [
            {
                'url': "https://play.embehub.com/SYFY/index.fmp4.m3u8",
                'title': "SYFY",
                'behaviorHints': {
                    'notWebReady': True,
                    'proxyHeaders': {
                        'request': {
                            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            'Referer': "https://play.embehub.com/SYFY/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:cinemax',
        'server': 'redecanais',
        'page': 'https://redecanaistv.ps/link/stream.m3u8?categoria=fhd&canal=c0hIM0JOclpXRllkRVRoQzNGQmg3U2JU',
        'type': 'tv',
        'name': 'CINEMAX',
        'poster': f"{server}https://embehub.com/img/thumb-cinemax.jpg",
        'background': f"{server}https://embehub.com/img/thumb-cinemax.jpg",
        'description': 'Canal CINEMAX ao vivo.',
        'genres': ['Filmes e Series'],
        'streams': [
            {
                'url': "",
                'title': "CINEMAX",
                'behaviorHints': {
                    'notWebReady': True,
                    'proxyHeaders': {
                        'request': {
                            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            'Origin': "https://redecanaistv.ps",
                            'Referer': "https://redecanaistv.ps/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:comedycentral",
        "type": "tv",
        "name": "COMEDY CENTRAL",
        "poster": f"{server}https://embehub.com/img/thumb-comedycentral.jpg",
        "background": f"{server}https://embehub.com/img/thumb-comedycentral.jpg",
        "description": "Canal COMEDY CENTRAL ao vivo.",
        "genres": ["Variedades"],
        "streams": [
            {
                "url": "https://anonstream.zip/comedycentral/index.m3u8",
                "title": "COMEDY CENTRAL",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://embedstream.org",
                            "Referer": "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:sony",
        "type": "tv",
        "name": "SONY CHANNEL",
        "poster": f"{server}https://embehub.com/img/thumb-sony.jpg",
        "background": f"{server}https://embehub.com/img/thumb-sony.jpg",
        "description": "SONY CHANNEL ao vivo.",
        "genres": ["Filmes e Series"],
        "streams": [
            {
                "url": "https://anonstream.zip/sonychannel/index.m3u8",
                "title": "SONY CHANNEL",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://embedstream.org",
                            "Referer": "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:starchannel",
        "type": "tv",
        "name": "STAR CHANNEL",
        "poster": f"{server}https://embehub.com/img/thumb-starchannel.jpg",
        "background": f"{server}https://embehub.com/img/thumb-starchannel.jpg",
        "description": "STAR CHANNEL ao vivo.",
        "genres": ["Filmes e Series"],
        "streams": [
            {
                "url": "https://anonstream.zip/starchannel/index.m3u8",
                "title": "STAR CHANNEL",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://embedstream.org",
                            "Referer": "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:warnertv",
        "type": "tv",
        "name": "WARNER TV",
        "poster": f"{server}https://embehub.com/img/thumb-warner.jpg",
        "background": f"{server}https://embehub.com/img/thumb-warner.jpg",
        "description": "canal WARNER TV ao vivo.",
        "genres": ["Filmes e Series"],
        "streams": [
            {
                "url": "https://anonstream.zip/warnerchannel/index.m3u8",
                "title": "WARNER TV",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://embedstream.org",
                            "Referer": "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:aie",
        "type": "tv",
        "name": "A&E",
        "poster": f"{server}https://embehub.com/img/A&E_Network_logo.png",
        "background": f"{server}https://embehub.com/img/A&E_Network_logo.png",
        "description": "canal A&E ao vivo.",
        "genres": ["Filmes e Series"],
        "streams": [
            {
                "url": "https://anonstream.zip/aee/index.m3u8",
                "title": "A&E",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://embedstream.org",
                            "Referer": "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:investigacao",
        "type": "tv",
        "name": "INVESTIGAÇÃO DISCOVERY",
        "poster": f"{server}https://embehub.com/img/iddiscovery.jpeg",
        "background": f"{server}https://embehub.com/img/iddiscovery.jpeg",
        "description": "canal INVESTIGAÇÃO DISCOVERY ao vivo.",
        "genres": ["Documentarios"],
        "streams": [
            {
                "url": "https://anonstream.zip/discoveryid/index.m3u8",
                "title": "INVESTIGAÇÃO DISCOVERY",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://embedstream.org",
                            "Referer": "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:tlc",
        "type": "tv",
        "name": "TLC",
        "poster": f"{server}https://embehub.com/img/discoverytlc.png",
        "background": f"{server}https://embehub.com/img/discoverytlc.png",
        "description": "canal TLC ao vivo.",
        "genres": ["Documentarios"],
        "streams": [
            {
                "url": "https://anonstream.zip/tlc/index.m3u8",
                "title": "TLC",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://embedstream.org",
                            "Referer": "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:megapix",
        "type": "tv",
        "name": "MEGAPIX",
        "poster": f"{server}https://embehub.com/img/megapix.jpg",
        "background": f"{server}https://embehub.com/img/megapix.jpg",
        "description": "canal MEGAPIX ao vivo.",
        "genres": ["Filmes e Series"],
        "streams": [
            {
                "url": "https://anonstream.zip/megapix/index.m3u8",
                "title": "MEGAPIX",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://embedstream.org",
                            "Referer": "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:studiouniversal",
        "type": "tv",
        "name": "STUDIO UNIVERSAL",
        "poster": f"{server}https://embehub.com/img/universalstudios.png",
        "background": f"{server}https://embehub.com/img/universalstudios.png",
        "description": "canal STUDIO UNIVERSAL ao vivo.",
        "genres": ["Filmes e Series"],
        "streams": [
            {
                "url": "https://anonstream.zip/studiouniversal/index.m3u8",
                "title": "STUDIO UNIVERSAL",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://embedstream.org",
                            "Referer": "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:lifetime",
        "type": "tv",
        "name": "LIFETIME",
        "poster": "https://i.ibb.co/jGXbx1x/lifetime.jpg",
        "background": "https://i.ibb.co/jGXbx1x/lifetime.jpg",
        "description": "canal LIFETIME ao vivo.",
        "genres": ["Filmes e Series"],
        "streams": [
            {
                "url": "https://play.embehub.com/lifetime/index.fmp4.m3u8",
                "title": "LIFETIME",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/lifetime/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:cinecanal",
        "type": "tv",
        "name": "CINE CANAL",
        "poster": "https://seeklogo.com/images/C/Cinecanal-logo-C68A0CF747-seeklogo.com.png",
        "background": "https://seeklogo.com/images/C/Cinecanal-logo-C68A0CF747-seeklogo.com.png",
        "description": "CINE CANAL ao vivo.",
        "genres": ["Filmes e Series"],
        "streams": [
            {
                "url": "https://anonstream.zip/cinecanal/index.m3u8",
                "title": "CINE CANAL",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://embedstream.org",
                            "Referer": "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:eentertainment",
        "type": "tv",
        "name": "!E",
        "poster": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/E%21_Logo.svg/1200px-E%21_Logo.svg.png",
        "background": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/E%21_Logo.svg/1200px-E%21_Logo.svg.png",
        "description": "canal !E ao vivo.",
        "genres": ["Variedades"],
        "streams": [
            {
                "url": "https://anonstream.zip/e/index.m3u8",
                "title": "!E",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://embedstream.org",
                            "Referer": "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:bandsports",
        "type": "tv",
        "name": "BANDSPORTS",
        "poster": f"{server}https://embehub.com/img/thumb-bandsports.jpg",
        "background": f"{server}https://embehub.com/img/thumb-bandsports.jpg",
        "description": "canal BANDSPORTS ao vivo.",
        "genres": ["Esportes"],
        "streams": [
            {
                "url": "https://anonstream.zip/bandsports/tracks-v1a1/mono.m3u8",
                "title": "BANDSPORTS",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://embedstream.org",
                            "Referer": "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:espn",
        "type": "tv",
        "name": "ESPN",
        "poster": f"{server}https://embehub.com/img/thumb-espn.jpg",
        "background": f"{server}https://embehub.com/img/thumb-espn.jpg",
        "description": "canal ESPN ao vivo.",
        "genres": ["Esportes"],
        "streams": [
            {
                "url": "https://super-cdn.link/espn/index.m3u8",
                "title": "ESPN",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://embedstream.org",
                            "Referer": "https://embedstream.org/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:espn2",
        "type": "tv",
        "name": "ESPN 2",
        "poster": f"{server}https://embehub.com/img/thumb-espn2.jpg",
        "background": f"{server}https://embehub.com/img/thumb-espn2.jpg",
        "description": "canal ESPN 2 ao vivo.",
        "genres": ["Esportes"],
        "streams": [
            {
                "url": "https://play.embehub.com/ESPN2/index.fmp4.m3u8",
                "title": "ESPN 2",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/ESPN2/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:espn3",
        "type": "tv",
        "name": "ESPN 3",
        "poster": f"{server}https://embehub.com/img/thumb-espn3.jpg",
        "background": f"{server}https://embehub.com/img/thumb-espn3.jpg",
        "description": "canal ESPN 3 ao vivo.",
        "genres": ["Esportes"],
        "streams": [
            {
                "url": "https://play.embehub.com/ESPN3/index.fmp4.m3u8",
                "title": "ESPN 3",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/ESPN3/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:espn4",
        "type": "tv",
        "name": "ESPN 4",
        "poster": f"{server}https://embehub.com/img/thumb-espn4.jpg",
        "background": f"{server}https://embehub.com/img/thumb-espn4.jpg",
        "description": "canal ESPN 4 ao vivo.",
        "genres": ["Esportes"],
        "streams": [
            {
                "url": "https://play.embehub.com/ESPN4/index.fmp4.m3u8",
                "title": "ESPN 4",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/ESPN4/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:espn5",
        "type": "tv",
        "name": "ESPN 5",
        "poster": f"{server}https://embehub.com/img/thumb-espn5.jpg",
        "background": f"{server}https://embehub.com/img/thumb-espn5.jpg",
        "description": "canal ESPN 5 ao vivo.",
        "genres": ["Esportes"],
        "streams": [
            {
                "url": "https://play.embehub.com/ESPN5/index.fmp4.m3u8",
                "title": "ESPN 5",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/ESPN5/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:espn6",
        "type": "tv",
        "name": "ESPN 6",
        "poster": f"{server}https://embehub.com/img/thumb-espn6.jpg",
        "background": f"{server}https://embehub.com/img/thumb-espn6.jpg",
        "description": "canal ESPN 6 ao vivo.",
        "genres": ["Esportes"],
        "streams": [
            {
                "url": "https://play.embehub.com/ESPN6/index.fmp4.m3u8",
                "title": "ESPN 6",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/ESPN6/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:sportv",
        "type": "tv",
        "name": "SPORTV",
        "poster": f"{server}https://embehub.com/img/thumb-sportv1.jpg",
        "background": f"{server}https://embehub.com/img/thumb-sportv1.jpg",
        "description": "canal SPORTV ao vivo.",
        "genres": ["Esportes"],
        "streams": [
            {
                "url": "https://play.embehub.com/SPORTTV1/index.fmp4.m3u8",
                "title": "SPORTV",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/SPORTTV1/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:sportv2",
        "type": "tv",
        "name": "SPORTV 2",
        "poster": f"{server}https://embehub.com/img/thumb-sportv2.jpg",
        "background": f"{server}https://embehub.com/img/thumb-sportv2.jpg",
        "description": "canal SPORTV 2 ao vivo.",
        "genres": ["Esportes"],
        "streams": [
            {
                "url": "https://play.embehub.com/SPORTTV2/index.fmp4.m3u8",
                "title": "SPORTV 2",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/SPORTTV2/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:sportv3",
        "type": "tv",
        "name": "SPORTV 3",
        "poster": f"{server}https://embehub.com/img/thumb-sportv3.jpg",
        "background": f"{server}https://embehub.com/img/thumb-sportv3.jpg",
        "description": "canal SPORTV 3 ao vivo.",
        "genres": ["Esportes"],
        "streams": [
            {
                "url": "https://play.embehub.com/SPORTTV3/index.fmp4.m3u8",
                "title": "SPORTV 3",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/SPORTTV3/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:premiereclubes",
        "type": "tv",
        "name": "PREMIERE CLUBES",
        "poster": f"{server}https://embehub.com/img/thumb-premiereclubes.jpg",
        "background": f"{server}https://embehub.com/img/thumb-premiereclubes.jpg",
        "description": "canal PREMIERE CLUBES ao vivo.",
        "genres": ["Esportes"],
        "streams": [
            {
                "url": "https://embedcanaistv.site/premiereclubes/video.m3u8",
                "title": "PREMIERE CLUBES",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://embedcanaistv.com",
                            "Referer": "https://embedcanaistv.com/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:premiere2",
        "type": "tv",
        "name": "PREMIERE 2",
        "poster": f"{server}https://embehub.com/img/thumb-premiere2.jpg",
        "background": f"{server}https://embehub.com/img/thumb-premiere2.jpg",
        "description": "canal PREMIERE 2 ao vivo.",
        "genres": ["Esportes"],
        "streams": [
            {
                "url": "https://embedcanaistv.site/premiere2/video.m3u8",
                "title": "PREMIERE 2",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://embedcanaistv.com",
                            "Referer": "https://embedcanaistv.com/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:premiere3",
        "type": "tv",
        "name": "PREMIERE 3",
        "poster": f"{server}https://embehub.com/img/thumb-premiere3.jpg",
        "background": f"{server}https://embehub.com/img/thumb-premiere3.jpg",
        "description": "canal PREMIERE 3 ao vivo.",
        "genres": ["Esportes"],
        "streams": [
            {
                "url": "https://play.embehub.com/PREMIERE3/index.fmp4.m3u8",
                "title": "PREMIERE 3",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/PREMIERE3/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:premiere4",
        "type": "tv",
        "name": "PREMIERE 4",
        "poster": f"{server}https://embehub.com/img/thumb-premiere4.jpg",
        "background": f"{server}https://embehub.com/img/thumb-premiere4.jpg",
        "description": "canal PREMIERE 4 ao vivo.",
        "genres": ["Esportes"],
        "streams": [
            {
                "url": "https://play.embehub.com/PREMIERE4/index.fmp4.m3u8",
                "title": "PREMIERE 4",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/PREMIERE4/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:premiere5",
        "type": "tv",
        "name": "PREMIERE 5",
        "poster": f"{server}https://embehub.com/img/thumb-premiere5.jpg",
        "background": f"{server}https://embehub.com/img/thumb-premiere5.jpg",
        "description": "canal PREMIERE 5 ao vivo.",
        "genres": ["Esportes"],
        "streams": [
            {
                "url": "https://embedcanaistv.site/premiere5/video.m3u8",
                "title": "PREMIERE 5",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://embedcanaistv.com",
                            "Referer": "https://embedcanaistv.com/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:premiere6",
        "type": "tv",
        "name": "PREMIERE 6",
        "poster": f"{server}https://embehub.com/img/thumb-premiere6.jpg",
        "background": f"{server}https://embehub.com/img/thumb-premiere6.jpg",
        "description": "canal PREMIERE 6 ao vivo.",
        "genres": ["Esportes"],
        "streams": [
            {
                "url": "https://embedcanaistv.site/premiere6/video.m3u8",
                "title": "PREMIERE 6",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://embedcanaistv.com",
                            "Referer": "https://embedcanaistv.com/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:premiere7",
        "type": "tv",
        "name": "PREMIERE 7",
        "poster": f"{server}https://embehub.com/img/thumb-premiere7.jpg",
        "background": f"{server}https://embehub.com/img/thumb-premiere7.jpg",
        "description": "canal PREMIERE 7 ao vivo.",
        "genres": ["Esportes"],
        "streams": [
            {
                "url": "https://play.embehub.com/PREMIERE7/index.fmp4.m3u8",
                "title": "PREMIERE 7",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/PREMIERE7/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:paramountplus",
        "type": "tv",
        "name": "PARAMOUNT+",
        "poster": f"{server}https://embehub.com/img/thumb-paramountplus1.jpg",
        "background": f"{server}https://embehub.com/img/thumb-paramountplus1.jpg",
        "description": "canal PARAMOUNT+ ao vivo.",
        "genres": ["Esportes"],
        "streams": [
            {
                "url": "https://play.embehub.com/PARAMOUNT+1/index.fmp4.m3u8",
                "title": "PARAMOUNT+",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/PARAMOUNT+1/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:paramountplus2',
        'type': 'tv',
        'name': 'PARAMOUNT+ 2',
        'poster': f"{server}https://embehub.com/img/thumb-paramountplus2.jpg",
        'background': f"{server}https://embehub.com/img/thumb-paramountplus2.jpg",
        'description': 'canal PARAMOUNT+ 2 ao vivo.',
        'genres': ['Esportes'],
        'streams': [
            {
                "url": "https://play.embehub.com/PARAMOUNT+2/index.fmp4.m3u8",
                "title": "PARAMOUNT+ 2",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/PARAMOUNT+2/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:paramountplus3',
        'type': 'tv',
        'name': 'PARAMOUNT+ 3',
        'poster': f"{server}https://embehub.com/img/thumb-paramountplus3.jpg",
        'background': f"{server}https://embehub.com/img/thumb-paramountplus3.jpg",
        'description': 'canal PARAMOUNT+ 3 ao vivo.',
        'genres': ['Esportes'],
        'streams': [
            {
                "url": "https://play.embehub.com/PARAMOUNT+3/index.fmp4.m3u8",
                "title": "PARAMOUNT+ 3",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/PARAMOUNT+3/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:paramountplus4',
        'type': 'tv',
        'name': 'PARAMOUNT+ 4',
        'poster': f"{server}https://embehub.com/img/thumb-paramountplus4.jpg",
        'background': f"{server}https://embehub.com/img/thumb-paramountplus4.jpg",
        'description': 'canal PARAMOUNT+ 4 ao vivo.',
        'genres': ['Esportes'],
        'streams': [
            {
                "url": "https://play.embehub.com/PARAMOUNT+4/index.fmp4.m3u8",
                "title": "PARAMOUNT+ 4",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/PARAMOUNT+4/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:combate',
        'type': 'tv',
        'name': 'COMBATE',
        'poster': f"{server}https://embehub.com/img/thumb-combate.jpg",
        'background': f"{server}https://embehub.com/img/thumb-combate.jpg",
        'description': 'canal COMBATE ao vivo.',
        'genres': ['Esportes'],
        'streams': [
            {
                "url": "https://play.embehub.com/COMBATE/index.fmp4.m3u8",
                "title": "COMBATE",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/COMBATE/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:cazetv1',
        'type': 'tv',
        'name': 'CAZE TV 1',
        'poster': f"{server}https://embehub.com/img/cazetv.png",
        'background': f"{server}https://embehub.com/img/cazetv.png",
        'description': 'canal CAZE TV 1 ao vivo.',
        'genres': ['Esportes'],
        'streams': [
            {
                "url": "https://play.embehub.com/CAZETV1/index.fmp4.m3u8",
                "title": "CAZE TV 1",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/CAZETV1/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:cazetv2',
        'type': 'tv',
        'name': 'CAZE TV 2',
        'poster': f"{server}https://embehub.com/img/cazetv.png",
        'background': f"{server}https://embehub.com/img/cazetv.png",
        'description': 'canal CAZE TV 2 ao vivo.',
        'genres': ['Esportes'],
        'streams': [
            {
                "url": "https://play.embehub.com/CAZETV2/index.fmp4.m3u8",
                "title": "CAZE TV 2",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/CAZETV2/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:cazetv3',
        'type': 'tv',
        'name': 'CAZE TV 3',
        'poster': f"{server}https://embehub.com/img/cazetv.png",
        'background': f"{server}https://embehub.com/img/cazetv.png",
        'description': 'canal CAZE TV 3 ao vivo.',
        'genres': ['Esportes'],
        'streams': [
            {
                "url": "https://play.embehub.com/CAZETV3/index.fmp4.m3u8",
                "title": "CAZE TV 3",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/CAZETV3/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:goat1',
        'type': 'tv',
        'name': 'CANAL GOAT 1',
        'poster': f"{server}https://embehub.com/img/canalgoat.jpg",
        'background': f"{server}https://embehub.com/img/canalgoat.jpg",
        'description': 'CANAL GOAT 1 ao vivo.',
        'genres': ['Esportes'],
        'streams': [
            {
                "url": "https://play.embehub.com/CANALGOAT1/index.fmp4.m3u8",
                "title": "CANAL GOAT 1",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/CANALGOAT1/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:goat2',
        'type': 'tv',
        'name': 'CANAL GOAT 2',
        'poster': f"{server}https://embehub.com/img/canalgoat.jpg",
        'background': f"{server}https://embehub.com/img/canalgoat.jpg",
        'description': 'CANAL GOAT 2 ao vivo.',
        'genres': ['Esportes'],
        'streams': [
            {
                "url": "https://play.embehub.com/CANALGOAT2/index.fmp4.m3u8",
                "title": "CANAL GOAT 2",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/CANALGOAT2/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:goat3',
        'type': 'tv',
        'name': 'CANAL GOAT 3',
        'poster': f"{server}https://embehub.com/img/canalgoat.jpg",
        'background': f"{server}https://embehub.com/img/canalgoat.jpg",
        'description': 'CANAL GOAT 3 ao vivo.',
        'genres': ['Esportes'],
        'streams': [
            {
                "url": "https://play.embehub.com/CANALGOAT3/index.fmp4.m3u8",
                "title": "CANAL GOAT 3",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/CANALGOAT3/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:goat4',
        'type': 'tv',
        'name': 'CANAL GOAT 4',
        'poster': f"{server}https://embehub.com/img/canalgoat.jpg",
        'background': f"{server}https://embehub.com/img/canalgoat.jpg",
        'description': 'CANAL GOAT 4 ao vivo.',
        'genres': ['Esportes'],
        'streams': [
            {
                "url": "https://play.embehub.com/CANALGOAT4/index.fmp4.m3u8",
                "title": "CANAL GOAT 4",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/CANALGOAT4/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:ufcfightpass1',
        'type': 'tv',
        'name': 'UFC FIGHT PASS 1',
        'poster': f"{server}https://embehub.com/img/thumb-ufcfightpass.jpg",
        'background': f"{server}https://embehub.com/img/thumb-ufcfightpass.jpg",
        'description': 'canal UFC FIGHT PASS 1 ao vivo.',
        'genres': ['Esportes'],
        'streams': [
            {
                "url": "https://play.embehub.com/UFCFIGHTPASS1/index.fmp4.m3u8",
                "title": "UFC FIGHT PASS 1",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/UFCFIGHTPASS1/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:ufcfightpass2',
        'type': 'tv',
        'name': 'UFC FIGHT PASS 2',
        'poster': f"{server}https://embehub.com/img/thumb-ufcfightpass.jpg",
        'background': f"{server}https://embehub.com/img/thumb-ufcfightpass.jpg",
        'description': 'canal UFC FIGHT PASS 2 ao vivo.',
        'genres': ['Esportes'],
        'streams': [
            {
                "url": "https://play.embehub.com/UFCFIGHTPASS2/index.fmp4.m3u8",
                "title": "UFC FIGHT PASS 2",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/UFCFIGHTPASS2/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:ufcfightpass3',
        'type': 'tv',
        'name': 'UFC FIGHT PASS 3',
        'poster': f"{server}https://embehub.com/img/thumb-ufcfightpass.jpg",
        'background': f"{server}https://embehub.com/img/thumb-ufcfightpass.jpg",
        'description': 'canal UFC FIGHT PASS 3 ao vivo.',
        'genres': ['Esportes'],
        'streams': [
            {
                "url": "https://play.embehub.com/UFCFIGHTPASS3/index.fmp4.m3u8",
                "title": "UFC FIGHT PASS 3",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/UFCFIGHTPASS3/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:disneyplus1',
        'type': 'tv',
        'name': 'DISNEY+ 1',
        'poster': f"{server}https://embehub.com/img/disney+.png",
        'background': f"{server}https://embehub.com/img/disney+.png",
        'description': 'canal DISNEY+ 1 ao vivo.',
        'genres': ['Esportes'],
        'streams': [
            {
                "url": "https://play.embehub.com/DISNEY+1/index.fmp4.m3u8",
                "title": "DISNEY+ 1",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/DISNEY+1/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:disneyplus2',
        'type': 'tv',
        'name': 'DISNEY+ 2',
        'poster': f"{server}https://embehub.com/img/disney+.png",
        'background': f"{server}https://embehub.com/img/disney+.png",
        'description': 'canal DISNEY+ 2 ao vivo.',
        'genres': ['Esportes'],
        'streams': [
            {
                "url": "https://play.embehub.com/DISNEY+2/index.fmp4.m3u8",
                "title": "DISNEY+ 2",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/DISNEY+2/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:disneyplus3',
        'type': 'tv',
        'name': 'DISNEY+ 3',
        'poster': f"{server}https://embehub.com/img/disney+.png",
        'background': f"{server}https://embehub.com/img/disney+.png",
        'description': 'canal DISNEY+ 3 ao vivo.',
        'genres': ['Esportes'],
        'streams': [
            {
                "url": "https://play.embehub.com/DISNEY+3/index.fmp4.m3u8",
                "title": "DISNEY+ 3",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/DISNEY+3/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:disneyplus4',
        'type': 'tv',
        'name': 'DISNEY+ 4',
        'poster': f"{server}https://embehub.com/img/disney+.png",
        'background': f"{server}https://embehub.com/img/disney+.png",
        'description': 'canal DISNEY+ 4 ao vivo.',
        'genres': ['Esportes'],
        'streams': [
            {
                "url": "https://play.embehub.com/DISNEY+4/index.fmp4.m3u8",
                "title": "DISNEY+ 4",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/DISNEY+4/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:disneyplus5',
        'type': 'tv',
        'name': 'DISNEY+ 5',
        'poster': f"{server}https://embehub.com/img/disney+.png",
        'background': f"{server}https://embehub.com/img/disney+.png",
        'description': 'canal DISNEY+ 5 ao vivo.',
        'genres': ['Esportes'],
        'streams': [
            {
                "url": "https://play.embehub.com/DISNEY+5/index.fmp4.m3u8",
                "title": "DISNEY+ 5",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/DISNEY+5/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:disneyplus6',
        'type': 'tv',
        'name': 'DISNEY+ 6',
        'poster': f"{server}https://embehub.com/img/disney+.png",
        'background': f"{server}https://embehub.com/img/disney+.png",
        'description': 'canal DISNEY+ 6 ao vivo.',
        'genres': ['Esportes'],
        'streams': [
            {
                "url": "https://play.embehub.com/DISNEY+6/index.fmp4.m3u8",
                "title": "DISNEY+ 6",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/DISNEY+6/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:eventosextra',
        'type': 'tv',
        'name': 'EVENTOS EXTRAS',
        'poster': "https://i.ibb.co/JFXgB2D/OIP.jpg",
        'background': "https://i.ibb.co/JFXgB2D/OIP.jpg",
        'description': 'canal EVENTOS EXTRAS ao vivo.',
        'genres': ['Esportes'],
        'streams': [
            {
                "url": "https://play.embehub.com/Eventos_Extras_01/index.fmp4.m3u8",
                "title": "EVENTOS EXTRAS",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/Eventos_Extras_01/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:dazn1',
        'type': 'tv',
        'name': 'DAZN 1',
        'poster': f"{server}https://embehub.com/img/Danz.png",
        'background': f"{server}https://embehub.com/img/Danz.png",
        'description': 'canal DAZN 1 ao vivo.',
        'genres': ['Esportes'],
        'streams': [
            {
                "url": "https://play.embehub.com/DAZN_1/index.fmp4.m3u8",
                "title": "DAZN 1",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/DAZN_1/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:dazn2',
        'type': 'tv',
        'name': 'DAZN 2',
        'poster': f"{server}https://embehub.com/img/Danz.png",
        'background': f"{server}https://embehub.com/img/Danz.png",
        'description': 'canal DAZN 2 ao vivo.',
        'genres': ['Esportes'],
        'streams': [
            {
                "url": "https://panel.embehub.com/DAZN_2/index.fmp4.m3u8",
                "title": "DAZN 2",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://panel.embehub.com/DAZN_2/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:dazn3',
        'type': 'tv',
        'name': 'DAZN 3',
        'poster': f"{server}https://embehub.com/img/Danz.png",
        'background': f"{server}https://embehub.com/img/Danz.png",
        'description': 'canal DAZN 3 ao vivo.',
        'genres': ['Esportes'],
        'streams': [
            {
                "url": "https://play.embehub.com/DAZN_3/index.fmp4.m3u8",
                "title": "DAZN 3",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/DAZN_3/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:dazn4',
        'type': 'tv',
        'name': 'DAZN 4',
        'poster': f"{server}https://embehub.com/img/Danz.png",
        'background': f"{server}https://embehub.com/img/Danz.png",
        'description': 'canal DAZN 4 ao vivo.',
        'genres': ['Esportes'],
        'streams': [
            {
                "url": "https://play.embehub.com/DAZN_4/index.fmp4.m3u8",
                "title": "DAZN 4",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/DAZN_4/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:cartoon',
        'type': 'tv',
        'name': 'CARTOON NETWORK',
        'poster': f"{server}https://embehub.com/img/thumb-cartoon.jpg",
        'background': f"{server}https://embehub.com/img/thumb-cartoon.jpg",
        'description': 'canal CARTOON NETWORK ao vivo.',
        'genres': ['Infantil'],
        'streams': [
            {
                "url": "https://embedcanaistv.club/cartoonnetwork/video.m3u8",
                "title": "CARTOON NETWORK",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://embedcanaistv.com",
                            "Referer": "https://embedcanaistv.com/"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:discoverykids',
        'type': 'tv',
        'name': 'DISCOVERY KIDS',
        'poster': f"{server}https://embehub.com/img/thumb-discoverykids.jpg",
        'background': f"{server}https://embehub.com/img/thumb-discoverykids.jpg",
        'description': 'canal DISCOVERY KIDS ao vivo.',
        'genres': ['Infantil'],
        'streams': [
            {
                "url": "https://play.embehub.com/DISCOVERY_kids/index.fmp4.m3u8",
                "title": "DISCOVERY KIDS",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/DISCOVERY_kids/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:disney',
        'type': 'tv',
        'name': 'DISNEY CHANNEL',
        'poster': f"{server}https://embehub.com/img/thumb-disney.jpg",
        'background': f"{server}https://embehub.com/img/thumb-disney.jpg",
        'description': 'canal DISNEY CHANNEL ao vivo.',
        'genres': ['Infantil'],
        'streams': [
            {
                "url": "https://play.embehub.com/disney_channel/index.fmp4.m3u8",
                "title": "DISNEY CHANNEL",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/disney_channel/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:nick',
        'type': 'tv',
        'name': 'NICKELODEON',
        'poster': f"{server}https://embehub.com/img/thumb-nick.jpg",
        'background': f"{server}https://embehub.com/img/thumb-nick.jpg",
        'description': 'canal NICKELODEON ao vivo.',
        'genres': ['Infantil'],
        'streams': [
            {
                "url": "https://play.embehub.com/Nickelodeon/index.fmp4.m3u8",
                "title": "NICKELODEON",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/Nickelodeon/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:nickjr',
        'type': 'tv',
        'name': 'NICK JR.',
        'poster': f"{server}https://embehub.com/img/thumb-nickjr.jpg",
        'background': f"{server}https://embehub.com/img/thumb-nickjr.jpg",
        'description': 'canal NICK JR. ao vivo.',
        'genres': ['Infantil'],
        'streams': [
            {
                "url": "https://play.embehub.com/NICK_JR/index.fmp4.m3u8",
                "title": "NICK JR.",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/NICK_JR/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:cartoonito',
        'type': 'tv',
        'name': 'CARTOONITO',
        'poster': f"{server}https://embehub.com/img/thumb-cartoonito.jpg",
        'background': f"{server}https://embehub.com/img/thumb-cartoonito.jpg",
        'description': 'canal CARTOONITO ao vivo.',
        'genres': ['Infantil'],
        'streams': [
            {
                "url": "https://play.embehub.com/cartoonito/index.fmp4.m3u8",
                "title": "CARTOONITO",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/cartoonito/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:globinho',
        'type': 'tv',
        'name': 'GLOBINHO',
        'poster': f"{server}https://embehub.com/img/globinho.png",
        'background': f"{server}https://embehub.com/img/globinho.png",
        'description': 'canal GLOBINHO ao vivo.',
        'genres': ['Infantil'],
        'streams': [
            {
                "url": "https://play.embehub.com/GLOOBINHO/index.fmp4.m3u8",
                "title": "GLOBINHO",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/GLOOBINHO/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:gloob',
        'type': 'tv',
        'name': 'GLOOB',
        'poster': f"{server}https://embehub.com/img/gloob.png",
        'background': f"{server}https://embehub.com/img/gloob.png",
        'description': 'canal GLOOB ao vivo.',
        'genres': ['Infantil'],
        'streams': [
            {
                "url": "https://play.embehub.com/GLOOB/index.fmp4.m3u8",
                "title": "GLOOB",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/GLOOB/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:bandnews',
        'type': 'tv',
        'name': 'BAND NEWS',
        'poster': f"{server}https://embehub.com/img/thumb-bandnews.jpg",
        'background': f"{server}https://embehub.com/img/thumb-bandnews.jpg",
        'description': 'canal BAND NEWS ao vivo.',
        'genres': ['Noticias'],
        'streams': [
            {
                "url": "https://play.embehub.com/BANDNEWS/index.fmp4.m3u8",
                "title": "BAND NEWS",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/BANDNEWS/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:cnnbrasil',
        'type': 'tv',
        'name': 'CNN BRASIL',
        'poster': f"{server}https://embehub.com/img/thumb-cnnbrasil.jpg",
        'background': f"{server}https://embehub.com/img/thumb-cnnbrasil.jpg",
        'description': 'canal CNN BRASIL ao vivo.',
        'genres': ['Noticias'],
        'streams': [
            {
                "url": "https://video01.soultv.com.br/cnnbrasil/cnnbrasil/chunklist_w2038826838.m3u8",
                "title": "CNN BRASIL",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://soultv.com.br",
                            "Referer": "https://soultv.com.br/"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:jovempannews',
        'type': 'tv',
        'name': 'JOVEM PAN NEWS',
        'poster': f"{server}https://embehub.com/img/jovempamnews.jpg",
        'background': f"{server}https://embehub.com/img/jovempamnews.jpg",
        'description': 'canal JOVEM PAN NEWS ao vivo.',
        'genres': ['Noticias'],
        'streams': [
            {
                "url": "https://play.embehub.com/JOVEMPANNEWS/index.fmp4.m3u8",
                "title": "JOVEM PAN NEWS",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/JOVEMPANNEWS/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:recordnews',
        'type': 'tv',
        'name': 'RECORD NEWS',
        'poster': f"{server}https://embehub.com/img/recordnews.png",
        'background': f"{server}https://embehub.com/img/recordnews.png",
        'description': 'canal RECORD NEWS ao vivo.',
        'genres': ['Noticias'],
        'streams': [
            {
                "url": "https://play.embehub.com/RECORDNEWS/index.fmp4.m3u8",
                "title": "RECORD NEWS",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/RECORDNEWS/index.fmp4.m3u8"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:globonews',
        'type': 'tv',
        'name': 'GLOBO NEWS',
        'poster': f"{server}https://embehub.com/imagens/globonews.png",
        'background': f"{server}https://embehub.com/imagens/globonews.png",
        'description': 'canal GLOBO NEWS ao vivo.',
        'genres': ['Noticias'],
        'streams': [
            {
                "url": "https://play.embehub.com/GLOBONEWS/index.fmp4.m3u8",
                "title": "GLOBO NEWS",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/GLOBONEWS/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:plutoanime',
        'type': 'tv',
        'name': 'PLUTO ANIME',
        'poster': f"{server}https://embehub.com/img/plutotv.png",
        'background': f"{server}https://embehub.com/img/plutotv.png",
        'description': 'canal PLUTO ANIME ao vivo.',
        'genres': ['PLUTO TV'],
        'streams': [
            {
                "url": "https://play.embehub.com/Anime/index.fmp4.m3u8",
                "title": "PLUTO ANIME",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/Anime/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:plutoanimeacao',
        'type': 'tv',
        'name': 'PLUTO ANIME AÇÃO',
        'poster': f"{server}https://embehub.com/img/plutotv.png",
        'background': f"{server}https://embehub.com/img/plutotv.png",
        'description': 'canal PLUTO ANIME AÇÃO ao vivo.',
        'genres': ['PLUTO TV'],
        'streams': [
            {
                "url": "https://play.embehub.com/Animeacao/index.fmp4.m3u8",
                "title": "PLUTO ANIME AÇÃO",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/Animeacao/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:betplutotv',
        'type': 'tv',
        'name': 'BET PLUTO TV',
        'poster': f"{server}https://embehub.com/img/plutotv.png",
        'background': f"{server}https://embehub.com/img/plutotv.png",
        'description': 'canal BET PLUTO TV ao vivo.',
        'genres': ['PLUTO TV'],
        'streams': [
            {
                "url": "https://play.embehub.com/BETPlutoTV/index.fmp4.m3u8",
                "title": "BET PLUTO TV",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/BETPlutoTV/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:plutotvcineclassicos',
        'type': 'tv',
        'name': 'PLUTO TV CINE CLASSICOS',
        'poster': f"{server}https://embehub.com/img/plutotv.png",
        'background': f"{server}https://embehub.com/img/plutotv.png",
        'description': 'canal PLUTO TV CINE CLASSICOS ao vivo.',
        'genres': ['PLUTO TV'],
        'streams': [
            {
                "url": "https://play.embehub.com/CineClassicos/index.fmp4.m3u8",
                "title": "PLUTO TV CINE CLASSICOS",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/CineClassicos/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:plutocinecomedia',
        'type': 'tv',
        'name': 'PLUTO CINE COMÉDIA',
        'poster': f"{server}https://embehub.com/img/plutotv.png",
        'background': f"{server}https://embehub.com/img/plutotv.png",
        'description': 'canal PLUTO CINE COMÉDIA ao vivo.',
        'genres': ['PLUTO TV'],
        'streams': [
            {
                "url": "https://play.embehub.com/CineComedia/index.fmp4.m3u8",
                "title": "PLUTO CINE COMÉDIA",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/CineComedia/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:plutocinedrama',
        'type': 'tv',
        'name': 'PLUTO CINE DRAMA',
        'poster': f"{server}https://embehub.com/img/plutotv.png",
        'background': f"{server}https://embehub.com/img/plutotv.png",
        'description': 'canal PLUTO CINE DRAMA ao vivo.',
        'genres': ['PLUTO TV'],
        'streams': [
            {
                "url": "https://play.embehub.com/CineDrama/index.fmp4.m3u8",
                "title": "PLUTO CINE DRAMA",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/CineDrama/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:plutocinefamilia',
        'type': 'tv',
        'name': 'PLUTO CINE FAMILIA',
        'poster': f"{server}https://embehub.com/img/plutotv.png",
        'background': f"{server}https://embehub.com/img/plutotv.png",
        'description': 'canal PLUTO CINE FAMILIA ao vivo.',
        'genres': ['PLUTO TV'],
        'streams': [
            {
                "url": "https://play.embehub.com/CineFamilia/index.fmp4.m3u8",
                "title": "PLUTO CINE FAMILIA",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/CineFamilia/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:plutocineromance',
        'type': 'tv',
        'name': 'PLUTO CINE ROMANCE',
        'poster': f"{server}https://embehub.com/img/plutotv.png",
        'background': f"{server}https://embehub.com/img/plutotv.png",
        'description': 'canal PLUTO CINE ROMANCE ao vivo.',
        'genres': ['PLUTO TV'],
        'streams': [
            {
                "url": "https://play.embehub.com/CineRomance/index.fmp4.m3u8",
                "title": "PLUTO CINE ROMANCE",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/CineRomance/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:plutocinesucessos',
        'type': 'tv',
        'name': 'PLUTO CINE SUCESSOS',
        'poster': f"{server}https://embehub.com/img/plutotv.png",
        'background': f"{server}https://embehub.com/img/plutotv.png",
        'description': 'canal PLUTO CINE SUCESSOS ao vivo.',
        'genres': ['PLUTO TV'],
        'streams': [
            {
                "url": "https://play.embehub.com/CineSucessos/index.fmp4.m3u8",
                "title": "PLUTO CINE SUCESSOS",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/CineSucessos/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:plutocineterror',
        'type': 'tv',
        'name': 'PLUTO CINE TERROR',
        'poster': f"{server}https://embehub.com/img/plutotv.png",
        'background': f"{server}https://embehub.com/img/plutotv.png",
        'description': 'canal PLUTO CINE TERROR ao vivo.',
        'genres': ['PLUTO TV'],
        'streams': [
            {
                "url": "https://play.embehub.com/CineTerror/index.fmp4.m3u8",
                "title": "PLUTO CINE TERROR",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/CineTerror/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:plutocomedia',
        'type': 'tv',
        'name': 'PLUTO COMÉDIA',
        'poster': f"{server}https://embehub.com/img/plutotv.png",
        'background': f"{server}https://embehub.com/img/plutotv.png",
        'description': 'canal PLUTO COMÉDIA ao vivo.',
        'genres': ['PLUTO TV'],
        'streams': [
            {
                "url": "https://play.embehub.com/Comedia/index.fmp4.m3u8",
                "title": "PLUTO COMÉDIA",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/Comedia/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:plutocomedycentral',
        'type': 'tv',
        'name': 'PLUTO COMEDY CENTRAL',
        'poster': f"{server}https://embehub.com/img/plutotv.png",
        'background': f"{server}https://embehub.com/img/plutotv.png",
        'description': 'canal PLUTO COMEDY CENTRAL ao vivo.',
        'genres': ['PLUTO TV'],
        'streams': [
            {
                "url": "https://play.embehub.com/ComedyCentral/index.fmp4.m3u8",
                "title": "PLUTO COMEDY CENTRAL",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/ComedyCentral/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:plutofilmesacao',
        'type': 'tv',
        'name': 'PLUTO FILMES AÇÃO',
        'poster': f"{server}https://embehub.com/img/plutotv.png",
        'background': f"{server}https://embehub.com/img/plutotv.png",
        'description': 'canal PLUTO FILMES AÇÃO ao vivo.',
        'genres': ['PLUTO TV'],
        'streams': [
            {
                "url": "https://play.embehub.com/FilmesAcao/index.fmp4.m3u8",
                "title": "PLUTO FILMES AÇÃO",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/FilmesAcao/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:plutofilmenacionais',
        'type': 'tv',
        'name': 'PLUTO FILMES NACIONAIS',
        'poster': f"{server}https://embehub.com/img/plutotv.png",
        'background': f"{server}https://embehub.com/img/plutotv.png",
        'description': 'canal PLUTO FILMES NACIONAIS ao vivo.',
        'genres': ['PLUTO TV'],
        'streams': [
            {
                "url": "https://play.embehub.com/FilmesNacionais/index.fmp4.m3u8",
                "title": "PLUTO FILMES NACIONAIS",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/FilmesNacionais/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:plutoinvestigacao',
        'type': 'tv',
        'name': 'PLUTO INVESTIGAÇÃO',
        'poster': f"{server}https://embehub.com/img/plutotv.png",
        'background': f"{server}https://embehub.com/img/plutotv.png",
        'description': 'canal PLUTO INVESTIGAÇÃO ao vivo.',
        'genres': ['PLUTO TV'],
        'streams': [
            {
                "url": "https://play.embehub.com/Investigacao/index.fmp4.m3u8",
                "title": "PLUTO INVESTIGAÇÃO",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/Investigacao/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:plutokids',
        'type': 'tv',
        'name': 'PLUTO KIDS',
        'poster': f"{server}https://embehub.com/img/plutotv.png",
        'background': f"{server}https://embehub.com/img/plutotv.png",
        'description': 'canal PLUTO KIDS ao vivo.',
        'genres': ['PLUTO TV'],
        'streams': [
            {
                "url": "https://play.embehub.com/PlutoKids/index.fmp4.m3u8",
                "title": "PLUTO KIDS",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/PlutoKids/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:plutonatureza',
        'type': 'tv',
        'name': 'PLUTO NATUREZA',
        'poster': f"{server}https://embehub.com/img/plutotv.png",
        'background': f"{server}https://embehub.com/img/plutotv.png",
        'description': 'canal PLUTO NATUREZA ao vivo.',
        'genres': ['PLUTO TV'],
        'streams': [
            {
                "url": "https://play.embehub.com/Plutonatureza/index.fmp4.m3u8",
                "title": "PLUTO NATUREZA",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/Plutonatureza/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:plutoretro',
        'type': 'tv',
        'name': 'PLUTO RETRÔ',
        'poster': f"{server}https://embehub.com/img/plutotv.png",
        'background': f"{server}https://embehub.com/img/plutotv.png",
        'description': 'canal PLUTO RETRÔ ao vivo.',
        'genres': ['PLUTO TV'],
        'streams': [
            {
                "url": "https://play.embehub.com/Plutoretro/index.fmp4.m3u8",
                "title": "PLUTO RETRÔ",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/Plutoretro/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:plutoshowsstingray',
        'type': 'tv',
        'name': 'PLUTO SHOWS POR STINGRAY',
        'poster': f"{server}https://embehub.com/img/plutotv.png",
        'background': f"{server}https://embehub.com/img/plutotv.png",
        'description': 'canal PLUTO SHOWS POR STINGRAY ao vivo.',
        'genres': ['PLUTO TV'],
        'streams': [
            {
                "url": "https://play.embehub.com/PlutoShowsporStingray/index.fmp4.m3u8",
                "title": "PLUTO SHOWS POR STINGRAY",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/PlutoShowsporStingray/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:plutomisterios',
        'type': 'tv',
        'name': 'PLUTO MISTÉRIOS',
        'poster': f"{server}https://embehub.com/img/plutotv.png",
        'background': f"{server}https://embehub.com/img/plutotv.png",
        'description': 'canal PLUTO MISTÉRIOS ao vivo.',
        'genres': ['PLUTO TV'],
        'streams': [
            {
                "url": "https://play.embehub.com/Plutomisterios/index.fmp4.m3u8",
                "title": "PLUTO MISTÉRIOS",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/Plutomisterios/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:24hvaiqcola',
        'type': 'tv',
        'name': '24H VAI QUE COLA',
        'poster': f"{server}https://embehub.com/img/canal24h.png",
        'background': f"{server}https://embehub.com/img/canal24h.png",
        'description': 'canal 24H VAI QUE COLA ao vivo.',
        'genres': ['CANAL 24H'],
        'streams': [
            {
                "url": "https://play.embehub.com/24H_vai_que_cola/index.fmp4.m3u8",
                "title": "24H VAI QUE COLA",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/24H_vai_que_cola/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:24hxena',
        'type': 'tv',
        'name': '24H XENA',
        'poster': f"{server}https://embehub.com/img/canal24h.png",
        'background': f"{server}https://embehub.com/img/canal24h.png",
        'description': 'canal 24H XENA ao vivo.',
        'genres': ['CANAL 24H'],
        'streams': [
            {
                "url": "https://play.embehub.com/24H_Xena/index.fmp4.m3u8",
                "title": "24H XENA",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/24H_Xena/embed.html"
                        }
                    }
                }
            }
        ]
    }, 
    {
        'id': 'skyflix:24hummaluco',
        'type': 'tv',
        'name': '24H UM MALUCO NO PEDAÇO',
        'poster': f"{server}https://embehub.com/img/canal24h.png",
        'background': f"{server}https://embehub.com/img/canal24h.png",
        'description': 'canal 24H UM MALUCO NO PEDAÇO ao vivo.',
        'genres': ['CANAL 24H'],
        'streams': [
            {
                "url": "https://play.embehub.com/24H_um_maluco_no_pedaco/index.fmp4.m3u8",
                "title": "24H UM MALUCO NO PEDAÇO",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/24H_um_maluco_no_pedaco/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:24htresespias',
        'type': 'tv',
        'name': '24H TRÊS ESPIÃS DEMAIS',
        'poster': f"{server}https://embehub.com/img/canal24h.png",
        'background': f"{server}https://embehub.com/img/canal24h.png",
        'description': 'canal 24H TRÊS ESPIÃS DEMAIS ao vivo.',
        'genres': ['CANAL 24H'],
        'streams': [
            {
                "url": "https://play.embehub.com/24H_tres_espias_demais/index.fmp4.m3u8",
                "title": "24H TRÊS ESPIÃS DEMAIS",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/24H_tres_espias_demais/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:24htodomundoodeia',
        'type': 'tv',
        'name': '24H TODO MUNDO ODEIA O CHRIS',
        'poster': f"{server}https://embehub.com/img/canal24h.png",
        'background': f"{server}https://embehub.com/img/canal24h.png",
        'description': 'canal 24H TODO MUNDO ODEIA O CHRIS ao vivo.',
        'genres': ['CANAL 24H'],
        'streams': [
            {
                "url": "https://play.embehub.com/24H_todo_mundo_odeia_o_chris/index.fmp4.m3u8",
                "title": "24H TODO MUNDO ODEIA O CHRIS",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/24H_todo_mundo_odeia_o_chris/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:24htartarugasninjas',
        'type': 'tv',
        'name': '24H TARTARUGAS NINJAS',
        'poster': f"{server}https://embehub.com/img/canal24h.png",
        'background': f"{server}https://embehub.com/img/canal24h.png",
        'description': 'canal 24H TARTARUGAS NINJAS ao vivo.',
        'genres': ['CANAL 24H'],
        'streams': [
            {
                "url": "https://play.embehub.com/24H_tartarugas_ninjas/index.fmp4.m3u8",
                "title": "24H TARTARUGAS NINJAS",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/24H_tartarugas_ninjas/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:24hsobrenatural',
        'type': 'tv',
        'name': '24H SOBRENATURAL',
        'poster': f"{server}https://embehub.com/img/canal24h.png",
        'background': f"{server}https://embehub.com/img/canal24h.png",
        'description': 'canal 24H SOBRENATURAL ao vivo.',
        'genres': ['CANAL 24H'],
        'streams': [
            {
                "url": "https://play.embehub.com/24H_Sobrenatural/index.fmp4.m3u8",
                "title": "24H SOBRENATURAL",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/24H_Sobrenatural/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:24hsmallville',
        'type': 'tv',
        'name': '24H SMALLVILLE',
        'poster': f"{server}https://embehub.com/img/canal24h.png",
        'background': f"{server}https://embehub.com/img/canal24h.png",
        'description': 'canal 24H SMALLVILLE ao vivo.',
        'genres': ['CANAL 24H'],
        'streams': [
            {
                "url": "https://play.embehub.com/24H_SMALLVILLE/index.fmp4.m3u8",
                "title": "24H SMALLVILLE",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/24H_SMALLVILLE/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:24hkenanekel',
        'type': 'tv',
        'name': '24H KENAN E KEL',
        'poster': f"{server}https://embehub.com/img/canal24h.png",
        'background': f"{server}https://embehub.com/img/canal24h.png",
        'description': 'canal 24H KENAN E KEL ao vivo.',
        'genres': ['CANAL 24H'],
        'streams': [
            {
                "url": "https://play.embehub.com/24H_Kenan_e_Kel/index.fmp4.m3u8",
                "title": "24H KENAN E KEL",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/24H_Kenan_e_Kel/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:24hhercules',
        'type': 'tv',
        'name': '24H HERCULES',
        'poster': f"{server}https://embehub.com/img/canal24h.png",
        'background': f"{server}https://embehub.com/img/canal24h.png",
        'description': 'canal 24H HERCULES ao vivo.',
        'genres': ['CANAL 24H'],
        'streams': [
            {
                "url": "https://play.embehub.com/24H_HeRCULES/index.fmp4.m3u8",
                "title": "24H HERCULES",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/24H_HeRCULES/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:24hapatroa',
        'type': 'tv',
        'name': '24H EU, A PATROA E AS CRIANÇAS',
        'poster': f"{server}https://embehub.com/img/canal24h.png",
        'background': f"{server}https://embehub.com/img/canal24h.png",
        'description': 'canal 24H EU, A PATROA E AS CRIANÇAS ao vivo.',
        'genres': ['CANAL 24H'],
        'streams': [
            {
                "url": "https://play.embehub.com/24H_A_PATROA_E_AS_CRIANCAS/index.fmp4.m3u8",
                "title": "24H EU, A PATROA E AS CRIANÇAS",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/24H_A_PATROA_E_AS_CRIANCAS/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:24hdoishomensemeio',
        'type': 'tv',
        'name': '24H DOIS HOMENS E MEIO',
        'poster': f"{server}https://embehub.com/img/canal24h.png",
        'background': f"{server}https://embehub.com/img/canal24h.png",
        'description': 'canal 24H DOIS HOMENS E MEIO ao vivo.',
        'genres': ['CANAL 24H'],
        'streams': [
            {
                "url": "https://play.embehub.com/24H_DOIS_HOMENS_E_MEIO/index.fmp4.m3u8",
                "title": "24H DOIS HOMENS E MEIO",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/24H_DOIS_HOMENS_E_MEIO/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:24hcaocoragem',
        'type': 'tv',
        'name': '24H CÃO CORAGEM',
        'poster': f"{server}https://embehub.com/img/canal24h.png",
        'background': f"{server}https://embehub.com/img/canal24h.png",
        'description': 'canal 24H CÃO CORAGEM ao vivo.',
        'genres': ['CANAL 24H'],
        'streams': [
            {
                "url": "https://play.embehub.com/24H_CAO_CORAGEM/index.fmp4.m3u8",
                "title": "24H CÃO CORAGEM",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/24H_CAO_CORAGEM/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:24hchaves',
        'type': 'tv',
        'name': '24H CHAVES',
        'poster': f"{server}https://embehub.com/img/canal24h.png",
        'background': f"{server}https://embehub.com/img/canal24h.png",
        'description': 'canal 24H CHAVES ao vivo.',
        'genres': ['CANAL 24H'],
        'streams': [
            {
                "url": "https://play.embehub.com/24H_Chaves/index.fmp4.m3u8",
                "title": "24H CHAVES",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/24H_Chaves/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:24hchapolimcolorado',
        'type': 'tv',
        'name': '24H CHAPOLIM COLORADO',
        'poster': f"{server}https://embehub.com/img/canal24h.png",
        'background': f"{server}https://embehub.com/img/canal24h.png",
        'description': 'canal 24H CHAPOLIM COLORADO ao vivo.',
        'genres': ['CANAL 24H'],
        'streams': [
            {
                "url": "https://play.embehub.com/24H_CHAPOLIM_COLORADO/index.fmp4.m3u8",
                "title": "24H CHAPOLIM COLORADO",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/24H_CHAPOLIM_COLORADO/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:24hbreakingbad',
        'type': 'tv',
        'name': '24H BREAKING BAD',
        'poster': f"{server}https://embehub.com/img/canal24h.png",
        'background': f"{server}https://embehub.com/img/canal24h.png",
        'description': 'canal 24H BREAKING BAD ao vivo.',
        'genres': ['CANAL 24H'],
        'streams': [
            {
                "url": "https://play.embehub.com/24H_BREAKING_BAD/index.fmp4.m3u8",
                "title": "24H BREAKING BAD",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/24H_BREAKING_BAD/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:24hagrandefamilia',
        'type': 'tv',
        'name': '24H A GRANDE FAMILIA',
        'poster': f"{server}https://embehub.com/img/canal24h.png",
        'background': f"{server}https://embehub.com/img/canal24h.png",
        'description': 'canal 24H A GRANDE FAMILIA ao vivo.',
        'genres': ['CANAL 24H'],
        'streams': [
            {
                "url": "https://play.embehub.com/24H_A_GRANDE_FAMILIA/index.fmp4.m3u8",
                "title": "24H A GRANDE FAMILIA",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/24H_A_GRANDE_FAMILIA/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:24hxman',
        'type': 'tv',
        'name': '24H X MAN',
        'poster': f"{server}https://embehub.com/img/canal24h.png",
        'background': f"{server}https://embehub.com/img/canal24h.png",
        'description': 'canal 24H X MAN ao vivo.',
        'genres': ['CANAL 24H'],
        'streams': [
            {
                "url": "https://play.embehub.com/24H_x_man/index.fmp4.m3u8",
                "title": "24H X MAN",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/24H_x_man/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:24htonejerry',
        'type': 'tv',
        'name': '24H TON E JERRY',
        'poster': f"{server}https://embehub.com/img/canal24h.png",
        'background': f"{server}https://embehub.com/img/canal24h.png",
        'description': 'canal 24H TON E JERRY ao vivo.',
        'genres': ['CANAL 24H'],
        'streams': [
            {
                "url": "https://play.embehub.com/24H_tom_e_jerry/index.fmp4.m3u8",
                "title": "24H TON E JERRY",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/24H_tom_e_jerry/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:24hsuperman',
        'type': 'tv',
        'name': '24H SUPERMAN',
        'poster': f"{server}https://embehub.com/img/canal24h.png",
        'background': f"{server}https://embehub.com/img/canal24h.png",
        'description': 'canal 24H SUPERMAN ao vivo.',
        'genres': ['CANAL 24H'],
        'streams': [
            {
                "url": "https://play.embehub.com/24H_SUPERMAN/index.fmp4.m3u8",
                "title": "24H SUPERMAN",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/24H_SUPERMAN/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:24hsuperchoque',
        'type': 'tv',
        'name': '24H SUPER CHOQUE',
        'poster': f"{server}https://embehub.com/img/canal24h.png",
        'background': f"{server}https://embehub.com/img/canal24h.png",
        'description': 'canal 24H SUPER CHOQUE ao vivo.',
        'genres': ['CANAL 24H'],
        'streams': [
            {
                "url": "https://play.embehub.com/24H_SUPER_CHOQUE/index.fmp4.m3u8",
                "title": "24H SUPER CHOQUE",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/24H_SUPER_CHOQUE/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:24hsouthpark',
        'type': 'tv',
        'name': '24H SOUTH PARK',
        'poster': f"{server}https://embehub.com/img/canal24h.png",
        'background': f"{server}https://embehub.com/img/canal24h.png",
        'description': 'canal 24H SOUTH PARK ao vivo.',
        'genres': ['CANAL 24H'],
        'streams': [
            {
                "url": "https://play.embehub.com/24H_SOUTH_PARK/index.fmp4.m3u8",
                "title": "24H SOUTH PARK",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/24H_SOUTH_PARK/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:24hscoobydoo',
        'type': 'tv',
        'name': '24H SCOOBY DOO',
        'poster': f"{server}https://embehub.com/img/canal24h.png",
        'background': f"{server}https://embehub.com/img/canal24h.png",
        'description': 'canal 24H SCOOBY DOO ao vivo.',
        'genres': ['CANAL 24H'],
        'streams': [
            {
                "url": "https://play.embehub.com/24H_SCOOBY_DOO/index.fmp4.m3u8",
                "title": "24H SCOOBY DOO",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/24H_SCOOBY_DOO/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:24hpokemon',
        'type': 'tv',
        'name': '24H POKEMON',
        'poster': f"{server}https://embehub.com/img/canal24h.png",
        'background': f"{server}https://embehub.com/img/canal24h.png",
        'description': 'canal 24H POKEMON ao vivo.',
        'genres': ['CANAL 24H'],
        'streams': [
            {
                "url": "https://play.embehub.com/24H_POKEMON/index.fmp4.m3u8",
                "title": "24H POKEMON",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/24H_POKEMON/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:24hpeppapig',
        'type': 'tv',
        'name': '24H PEPPA PIG',
        'poster': f"{server}https://embehub.com/img/canal24h.png",
        'background': f"{server}https://embehub.com/img/canal24h.png",
        'description': 'canal 24H PEPPA PIG ao vivo.',
        'genres': ['CANAL 24H'],
        'streams': [
            {
                "url": "https://play.embehub.com/24H_PEPPA_PIG/index.fmp4.m3u8",
                "title": "24H PEPPA PIG",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/24H_PEPPA_PIG/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:24hossimpsons',
        'type': 'tv',
        'name': '24H OS SIMPSONS',
        'poster': f"{server}https://embehub.com/img/canal24h.png",
        'background': f"{server}https://embehub.com/img/canal24h.png",
        'description': 'canal 24H OS SIMPSONS ao vivo.',
        'genres': ['CANAL 24H'],
        'streams': [
            {
                "url": "https://play.embehub.com/24H_OS_SIMPSONS/index.fmp4.m3u8",
                "title": "24H OS SIMPSONS",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/24H_OS_SIMPSONS/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:24hcavernadodragao',
        'type': 'tv',
        'name': '24H CAVERNA DO DRAGÃO',
        'poster': f"{server}https://embehub.com/img/canal24h.png",
        'background': f"{server}https://embehub.com/img/canal24h.png",
        'description': 'canal 24H CAVERNA DO DRAGÃO ao vivo.',
        'genres': ['CANAL 24H'],
        'streams': [
            {
                "url": "https://play.embehub.com/24H_CAVERNA_DO_DRAGAO/index.fmp4.m3u8",
                "title": "24H CAVERNA DO DRAGÃO",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/24H_CAVERNA_DO_DRAGAO/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:24hnarutoshippuden',
        'type': 'tv',
        'name': '24H NARUTO SHIPPUDEN',
        'poster': f"{server}https://embehub.com/img/canal24h.png",
        'background': f"{server}https://embehub.com/img/canal24h.png",
        'description': 'canal 24H NARUTO SHIPPUDEN ao vivo.',
        'genres': ['CANAL 24H'],
        'streams': [
            {
                "url": "https://play.embehub.com/24H_NARUTO_SHIPPUDEN/index.fmp4.m3u8",
                "title": "24H NARUTO SHIPPUDEN",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/24H_NARUTO_SHIPPUDEN/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:24hnaruto',
        'type': 'tv',
        'name': '24H NARUTO',
        'poster': f"{server}https://embehub.com/img/canal24h.png",
        'background': f"{server}https://embehub.com/img/canal24h.png",
        'description': 'canal 24H NARUTO ao vivo.',
        'genres': ['CANAL 24H'],
        'streams': [
            {
                "url": "https://play.embehub.com/24H_Naruto/index.fmp4.m3u8",
                "title": "24H NARUTO",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/24H_Naruto/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:24hdragonballz',
        'type': 'tv',
        'name': '24H DRAGON BALL Z',
        'poster': f"{server}https://embehub.com/img/canal24h.png",
        'background': f"{server}https://embehub.com/img/canal24h.png",
        'description': 'canal 24H DRAGON BALL Z ao vivo.',
        'genres': ['CANAL 24H'],
        'streams': [
            {
                "url": "https://play.embehub.com/24H_DRAGON_BALL_Z/index.fmp4.m3u8",
                "title": "24H DRAGON BALL Z",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/24H_DRAGON_BALL_Z/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:24hdragonsuper',
        'type': 'tv',
        'name': '24H DRAGON SUPER',
        'poster': f"{server}https://embehub.com/img/canal24h.png",
        'background': f"{server}https://embehub.com/img/canal24h.png",
        'description': 'canal 24H DRAGON SUPER ao vivo.',
        'genres': ['CANAL 24H'],
        'streams': [
            {
                "url": "https://play.embehub.com/24H_DRAGON_SUPER/index.fmp4.m3u8",
                "title": "24H DRAGON SUPER",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/24H_DRAGON_SUPER/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:24hdragonball',
        'type': 'tv',
        'name': '24H DRAGON BALL',
        'poster': f"{server}https://embehub.com/img/canal24h.png",
        'background': f"{server}https://embehub.com/img/canal24h.png",
        'description': 'canal 24H DRAGON BALL ao vivo.',
        'genres': ['CANAL 24H'],
        'streams': [
            {
                "url": "https://play.embehub.com/24H_DRAGON_BALL/index.fmp4.m3u8",
                "title": "24H DRAGON BALL",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/24H_DRAGON_BALL/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:24hchavesdesenho',
        'type': 'tv',
        'name': '24H CHAVES DESENHO',
        'poster': f"{server}https://embehub.com/img/canal24h.png",
        'background': f"{server}https://embehub.com/img/canal24h.png",
        'description': 'canal 24H CHAVES DESENHO ao vivo.',
        'genres': ['CANAL 24H'],
        'streams': [
            {
                "url": "https://play.embehub.com/24H_CHAVES_DESENHO/index.fmp4.m3u8",
                "title": "24H CHAVES DESENHO",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/24H_CHAVES_DESENHO/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:24hbobesponja',
        'type': 'tv',
        'name': '24H BOB ESPONJA',
        'poster': f"{server}https://embehub.com/img/canal24h.png",
        'background': f"{server}https://embehub.com/img/canal24h.png",
        'description': 'canal 24H BOB ESPONJA ao vivo.',
        'genres': ['CANAL 24H'],
        'streams': [
            {
                "url": "https://play.embehub.com/24H_BOB_ESPONJA/index.fmp4.m3u8",
                "title": "24H BOB ESPONJA",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/24H_BOB_ESPONJA/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:bbb25cam1',
        'type': 'tv',
        'name': 'BBB 25 CAM 1',
        'poster': f"{server}https://embehub.com/img/bbb25.png",
        'background': f"{server}https://embehub.com/img/bbb25.png",
        'description': 'canal BBB 25 CAM 1 ao vivo.',
        'genres': ['Variedades'],
        'streams': [
            {
                "url": "https://redecanaistv.ps/link/stream.m3u8?categoria=fhd&canal=c0hIM0JOclpXRllkRVRoQzNGQmg3U2JU",
                "title": "BBB 25 CAM 1"
            }
        ]
    },
    {
        'id': 'skyflix:bbb25cam2',
        'type': 'tv',
        'name': 'BBB 25 CAM 2',
        'poster': f"{server}https://embehub.com/img/bbb25.png",
        'background': f"{server}https://embehub.com/img/bbb25.png",
        'description': 'canal BBB 25 CAM 2 ao vivo.',
        'genres': ['Variedades'],
        'streams': [
            {
                "url": "https://play.embehub.com/bbbcam02/index.fmp4.m3u8",
                "title": "BBB 25 CAM 2",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/bbbcam02/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:bbb25cam3',
        'type': 'tv',
        'name': 'BBB 25 CAM 3',
        'poster': f"{server}https://embehub.com/img/bbb25.png",
        'background': f"{server}https://embehub.com/img/bbb25.png",
        'description': 'canal BBB 25 CAM 3 ao vivo.',
        'genres': ['Variedades'],
        'streams': [
            {
                "url": "https://play.embehub.com/bbbcam03/index.fmp4.m3u8",
                "title": "BBB 25 CAM 3",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/bbbcam03/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:bbb25cam4',
        'type': 'tv',
        'name': 'BBB 25 CAM 4',
        'poster': f"{server}https://embehub.com/img/bbb25.png",
        'background': f"{server}https://embehub.com/img/bbb25.png",
        'description': 'canal BBB 25 CAM 4 ao vivo.',
        'genres': ['Variedades'],
        'streams': [
            {
                "url": "https://play.embehub.com/bbbcam04/index.fmp4.m3u8",
                "title": "BBB 25 CAM 4",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/bbbcam04/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:bbb25cam5',
        'type': 'tv',
        'name': 'BBB 25 CAM 5',
        'poster': f"{server}https://embehub.com/img/bbb25.png",
        'background': f"{server}https://embehub.com/img/bbb25.png",
        'description': 'canal BBB 25 CAM 5 ao vivo.',
        'genres': ['Variedades'],
        'streams': [
            {
                "url": "https://play.embehub.com/bbbcam05/index.fmp4.m3u8",
                "title": "BBB 25 CAM 5",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/bbbcam05/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:bbb25cam6',
        'type': 'tv',
        'name': 'BBB 25 CAM 6',
        'poster': f"{server}https://embehub.com/img/bbb25.png",
        'background': f"{server}https://embehub.com/img/bbb25.png",
        'description': 'canal BBB 25 CAM 6 ao vivo.',
        'genres': ['Variedades'],
        'streams': [
            {
                "url": "https://play.embehub.com/bbbcam06/index.fmp4.m3u8",
                "title": "BBB 25 CAM 6",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/bbbcam06/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:bbb25cam7',
        'type': 'tv',
        'name': 'BBB 25 CAM 7',
        'poster': f"{server}https://embehub.com/img/bbb25.png",
        'background': f"{server}https://embehub.com/img/bbb25.png",
        'description': 'canal BBB 25 CAM 7 ao vivo.',
        'genres': ['Variedades'],
        'streams': [
            {
                "url": "https://play.embehub.com/bbbcam07/index.fmp4.m3u8",
                "title": "BBB 25 CAM 7",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/bbbcam07/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:bbb25cam8',
        'type': 'tv',
        'name': 'BBB 25 CAM 8',
        'poster': f"{server}https://embehub.com/img/bbb25.png",
        'background': f"{server}https://embehub.com/img/bbb25.png",
        'description': 'canal BBB 25 CAM 8 ao vivo.',
        'genres': ['Variedades'],
        'streams': [
            {
                "url": "https://play.embehub.com/bbbcam08/index.fmp4.m3u8",
                "title": "BBB 25 CAM 8",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/bbbcam08/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:bbb25cam9',
        'type': 'tv',
        'name': 'BBB 25 CAM 9',
        'poster': f"{server}https://embehub.com/img/bbb25.png",
        'background': f"{server}https://embehub.com/img/bbb25.png",
        'description': 'canal BBB 25 CAM 9 ao vivo.',
        'genres': ['Variedades'],
        'streams': [
            {
                "url": "https://play.embehub.com/bbbcam09/index.fmp4.m3u8",
                "title": "BBB 25 CAM 9",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/bbbcam09/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:bbb25cam10',
        'type': 'tv',
        'name': 'BBB 25 CAM 10',
        'poster': f"{server}https://embehub.com/img/bbb25.png",
        'background': f"{server}https://embehub.com/img/bbb25.png",
        'description': 'canal BBB 25 CAM 10 ao vivo.',
        'genres': ['Variedades'],
        'streams': [
            {
                "url": "https://play.embehub.com/bbbcam10/index.fmp4.m3u8",
                "title": "BBB 25 CAM 10",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/bbbcam10/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:bbb25mosaico',
        'type': 'tv',
        'name': 'BBB 25 MOSAICO',
        'poster': f"{server}https://embehub.com/img/bbb25.png",
        'background': f"{server}https://embehub.com/img/bbb25.png",
        'description': 'canal BBB 25 MOSAICO ao vivo.',
        'genres': ['Variedades'],
        'streams': [
            {
                "url": "https://play.embehub.com/bbbmosaico/index.fmp4.m3u8",
                "title": "BBB 25 MOSAICO",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Referer": "https://play.embehub.com/bbbmosaico/embed.html"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:kpoptv',
        'type': 'tv',
        'name': 'KPOP TV',
        'poster': f"{server}https://kpoptv.htforum.net/wp-content/uploads/2024/11/logokpoptvplay.png",
        'background': f"{server}https://kpoptv.htforum.net/wp-content/uploads/2024/11/logokpoptvplay.png",
        'description': 'canal KPOP TV ao vivo.',
        'genres': ['Variedades'],
        'streams': [
            {
                "url": "https://giatv.bozztv.com/giatv/giatv-kpoptvplay/kpoptvplay/playlist.m3u8",
                "title": "KPOP TV",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
                        }
                    }
                }
            }
        ]
    }, 
    {
        'id': 'skyflix:timesbrasil',
        'type': 'tv',
        'name': 'TIMES BRASIL | CNBC',
        'poster': f"{server}https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Times_Brasil_CNBC_logo.svg/2560px-Times_Brasil_CNBC_logo.svg.png",
        'background': f"{server}https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Times_Brasil_CNBC_logo.svg/2560px-Times_Brasil_CNBC_logo.svg.png",
        'description': 'canal TIMES BRASIL | CNBC ao vivo.',
        'genres': ['Noticias'],
        'streams': [
            {
                "url": "https://video01.soultv.com.br/timesbrasil/timesbrasil/chunklist_w1994015498.m3u8",
                "title": "TIMES BRASIL | CNBC",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://soultv.com.br",
                            "Referer": "https://soultv.com.br/"
                        }
                    }
                }
            }
        ]
    }                                                                                                                           
    ]
    return canais
 
 