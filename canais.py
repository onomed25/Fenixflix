import requests
import re
from urllib.parse import quote_plus, quote
from bs4 import BeautifulSoup
import base64

def canais_list(server):
    canais = [
    {
        "id": "skyflix:globosp",
        "rc": {"token": "c0hIM0JOdmVXVk1VRmpoRDJseHI4emM9", "channel": "bobosp"},
        "type": "tv",
        "name": "Globo SP",
        "poster": f"{server}https://embehub.com/img/globo.png",
        "background": f"{server}https://embehub.com/img/globo.png",
        "description": "Canal Globo SP ao vivo.",
        "genres": ["Canais Abertos"],
        "streams": [
            {
                "url": "",
                "title": "Globo SP",
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
        "id": "skyflix:globonordeste",
        "rc": {"token": "c0hIM0JOdmVVRmNZRkRoRDJseHI3aWpaZzloZ0Z6UT0=", "channel": "bobonordeste"},        
        "type": "tv",
        "name": "Globo Nordeste",
        "poster": f"{server}https://embehub.com/img/globo.png",
        "background": f"{server}https://embehub.com/img/globo.png",
        "description": "Canal Globo Nordeste ao vivo.",
        "genres": ["Canais Abertos"],
        "streams": [
            {
                "url": "",
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
        "rc": {"token": "c0hIM0JOclVXVlljRWpoUzEwbz0=", "channel": "sbt"},  
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
        "rc": {"token": "c0hIM0JOdmRWRmNZRmpoRDFGQmc=", "channel": "band"},         
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
        "rc": {"token": "c0hIM0JOclVWMWNWRnpoVDBGcGg5REU9", "channel": "redetv"},        
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
        "rc": {"token": "c0hIM0JOdlZVVmNZR3poVDBGMXI4aU09", "channel": "record"}, 
        "type": "tv",
        "name": "RECORD SP",
        "poster": f"{server}https://embehub.com/img/thumb-record.jpg",
        "background": f"{server}https://embehub.com/img/thumb-record.jpg",
        "description": "Canal RECORD SP ao vivo.",
        "genres": ["Canais Abertos"],
        "streams": [
            {
                "url": "",
                "title": "RECORD SP",
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
        "id": "skyflix:viva",
        "rc": {"token": "c0hIM0JOdlZVRk1mRVRoWDNFaGw=", "channel": "viva"},
        "type": "tv",
        "name": "VIVA",
        "poster": f"{server}https://embehub.com/img/thumb-viva.jpg",
        "background": f"{server}https://embehub.com/img/thumb-viva.jpg",
        "description": "Canal VIVA ao vivo.",
        "genres": ["Variedades"],
        "streams": [
            {
                "url": "",
                "title": "VIVA",
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
        "id": "skyflix:bis",
        "rc": {"token": "c0hIM0JOdlZWMVFZRnpoRDNFMD0=", "channel": "bis"},
        "type": "tv",
        "name": "BIS",
        "poster": f"{server}https://embehub.com/img/biz.png",
        "background": f"{server}https://embehub.com/img/biz.png",
        "description": "Canal BIS ao vivo.",
        "genres": ["Variedades"],
        "streams": [
            {
                "url": "",
                "title": "BIS",
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
        "id": "skyflix:gnt",
        "rc": {"token": "c0hIM0JOdlVWRnNmR3poRzIwbz0=", "channel": "gnt"},
        "type": "tv",
        "name": "GNT",
        "poster": f"{server}https://embehub.com/img/gnt.jpg",
        "background": f"{server}https://embehub.com/img/gnt.jpg",
        "description": "Canal GNT ao vivo.",
        "genres": ["Variedades"],
        "streams": [
            {
                "url": "",
                "title": "GNT",
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
        "id": "skyflix:multishow",
        "rc": {"token": "c0hIM0JOdlZVbG9ZRURoTXdGSnc2VFREaU1vPQ==", "channel": "multishow"},
        "type": "tv",
        "name": "MULTISHOW",
        "poster": f"{server}https://embehub.com/img/multishow.png",
        "background": f"{server}https://embehub.com/img/multishow.png",
        "description": "Canal MULTISHOW ao vivo.",
        "genres": ["Variedades"],
        "streams": [
            {
                "url": "",
                "title": "MULTISHOW",
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
        "id": "skyflix:off",
        "rc": {"token": "c0hIM0JOdlVXRk1jRlRoTzAxZz0=", "channel": "off"},
        "type": "tv",
        "name": "CANAL OFF",
        "poster": f"{server}https://embehub.com/img/canaloff.webp",
        "background": f"{server}https://embehub.com/img/canaloff.webp",
        "description": "Canal OFF ao vivo.",
        "genres": ["Variedades"],
        "streams": [
            {
                "url": "",
                "title": "CANAL OFF",
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
        "id": "skyflix:adultswim",
        "rc": {"token": "c0hIM0JOdmFXRklVRkRoQTBVdG85RFRjanRBPQ==", "channel": "adultswim"},
        "type": "tv",
        "name": "ADULT SWIM",
        "poster": f"{server}https://embehub.com/img/thumb-adultswim.jpg",
        "background": f"{server}https://embehub.com/img/thumb-adultswim.jpg",
        "description": "Canal ADULT SWIM ao vivo.",
        "genres": ["Variedades"],
        "streams": [
            {
                "url": "",
                "title": "MULTISHOW",
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
        "id": "skyflix:amc",
        "rc": {"token": "c0hIM0JOdmZWRmNiRURoQTJGMD0=", "channel": "amc"}, 
        "type": "tv",
        "name": "AMC",
        "poster": f"{server}https://embehub.com/img/AMC.jpg",
        "background": f"{server}https://embehub.com/img/AMC.jpg",
        "description": "Canal AMC ao vivo.",
        "genres": ["Filmes e Series"],
        "streams": [
            {
                "url": "",
                "title": "AMC",
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
        "id": "skyflix:animalplanet",
        "rc": {"token": "c0hIM0JOdlZXRmNkRmpoQTIxZHA0U3ZiaTl4OUJpVT0=", "channel": "animalplanet"},
        "type": "tv",
        "name": "ANIMAL PLANET",
        "poster": f"{server}https://embehub.com/img/thumb-animalplanet.jpg",
        "background": f"{server}https://embehub.com/img/thumb-animalplanet.jpg",
        "description": "Canal ANIMAL PLANET ao vivo.",
        "genres": ["Documentarios"],
        "streams": [
            {
                "url": "",
                "title": "ANIMAL PLANET",
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
        "id": "skyflix:arte1",
        "rc": {"token": "c0hIM0JOdmVWVllkRVRoQXgwcGhzUT09", "channel": "arte1"}, 
        "type": "tv",
        "name": "ARTE 1",
        "poster": f"{server}https://embehub.com/img/thumb-arte1.jpg",
        "background": f"{server}https://embehub.com/img/thumb-arte1.jpg",
        "description": "Canal ARTE 1 ao vivo.",
        "genres": ["Filmes e Series"],
        "streams": [
            {
                "url": "",
                "title": "ARTE 1",
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
        "id": "skyflix:axn",
        "rc": {"token": "c0hIM0JOdmZWRmNmRlRoQXpWQT0=", "channel": "axn"},
        "type": "tv",
        "name": "AXN",
        "poster": f"{server}https://embehub.com/img/thumb-axn.jpg",
        "background": f"{server}https://embehub.com/img/thumb-axn.jpg",
        "description": "Canal AXN ao vivo.",
        "genres": ["Filmes e Series"],
        "streams": [
            {
                "url": "",
                "title": "AXN",
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
        "id": "skyflix:canalbrasil",
        "rc": {"token": "c0hIM0JOdmZVbG9kRlRoQzFGQmw3Q1haaHM1NkR3PT0=", "channel": "canalbrasil"},
        "type": "tv",
        "name": "CANAL BRASIL",
        "poster": f"{server}https://embehub.com/img/thumb-canalbrasil.jpg",
        "background": f"{server}https://embehub.com/img/thumb-canalbrasil.jpg",
        "description": "Canal BRASIL ao vivo.",
        "genres": ["Filmes e Series"],
        "streams": [
            {
                "url": "",
                "title": "CANAL BRASIL",
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
        "id": "skyflix:discoverychannel",
        "rc": {"token": "c0hIM0JOdlZVVm9kRkRoRjNFMW43ekhPbGNRPQ==", "channel": "discovery"},
        "type": "tv",
        "name": "DISCOVERY CHANNEL",
        "poster": f"{server}https://embehub.com/img/thumb-discovery.jpg",
        "background": f"{server}https://embehub.com/img/thumb-discovery.jpg",
        "description": "Canal DISCOVERY CHANNEL ao vivo.",
        "genres": ["Documentarios"],
        "streams": [
            {
                "url": "",
                "title": "DISCOVERY CHANNEL",
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
        "id": "skyflix:discoveryheh",
        "rc": {"token": "c0hIM0JOdlVWRk1aRWpoRjNFMW43ekhPbGNSN0REejdNUWptZWdYKy9nPT0=", "channel": "discoveryhomeihealth"},
        "type": "tv",
        "name": "DISCOVERY HOME & HEALTH",
        "poster": f"{server}https://embehub.com/img/thumb-discoveryhomeihealth.jpg",
        "background": f"{server}https://embehub.com/img/thumb-discoveryhomeihealth.jpg",
        "description": "Canal DISCOVERY HOME & HEALTH ao vivo.",
        "genres": ["Documentarios"],
        "streams": [
            {
                "url": "",
                "title": "DISCOVERY HOME & HEALTH",
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
        "id": "skyflix:discoveryturbo",
        "rc": {"token": "c0hIM0JOdlZXRkFjRmpoRjNFMW43ekhPbGNSbkZpUDhOdz09", "channel": "discoveryturbo"},
        "type": "tv",
        "name": "DISCOVERY TURBO",
        "poster": f"{server}https://embehub.com/img/discoveryturbo.png",
        "background": f"{server}https://embehub.com/img/discoveryturbo.png",
        "description": "Canal DISCOVERY TURBO ao vivo.",
        "genres": ["Documentarios"],
        "streams": [
            {
                "url": "",
                "title": "DISCOVERY TURBO",
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
        "id": "skyflix:discoverytheater",
        "rc": {"token": "c0hIM0JOdlVVMU1WRnpoRjNFMW43ekhPbGNSbkN6VC9MQVh4", "channel": "discoverytheater"},
        "type": "tv",
        "name": "DISCOVERY THEATER",
        "poster": f"{server}https://embehub.com/img/discoverytheather.webp",
        "background": f"{server}https://embehub.com/img/discoverytheather.webp",
        "description": "Canal DISCOVERY THEATER ao vivo.",
        "genres": ["Documentarios"],
        "streams": [
            {
                "url": "",
                "title": "DISCOVERY THEATER",
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
        "id": "skyflix:discoveryworld",
        "rc": {"token": "c0hIM0JOdlZWbFFmRURoRjNFMW43ekhPbGNSa0RDUHlQQT09", "channel": "discoveryworld"},
        "type": "tv",
        "name": "DISCOVERY WORLD",
        "poster": f"{server}https://embehub.com/img/discoveryworld.png",
        "background": f"{server}https://embehub.com/img/discoveryworld.png",
        "description": "Canal DISCOVERY WORLD ao vivo.",
        "genres": ["Documentarios"],
        "streams": [
            {
                "url": "",
                "title": "DISCOVERY WORLD",
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
        "id": "skyflix:discoveryscience",
        "rc": {"token": "c0hIM0JOdmFXRlFjRVRoRjNFMW43ekhPbGNSZ0NqVHdPd1U9", "channel": "discoverysience"},
        "type": "tv",
        "name": "DISCOVERY SCIENCE",
        "poster": "https://static.wikia.nocookie.net/logopedia/images/6/63/Discovery_Science_LA_2011.png",
        "background": "https://static.wikia.nocookie.net/logopedia/images/6/63/Discovery_Science_LA_2011.png",
        "description": "canal DISCOVERY SCIENCE ao vivo.",
        "genres": ["Documentarios"],
        "streams": [
            {
                "url": "",
                "title": "DISCOVERY SCIENCE",
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
        "rc": {"token": "c0hIM0JOdmZVVlFkRlRoSjExRT0=", "channel": "hbo"},
        "type": "tv",
        "name": "HBO",
        "poster": f"{server}https://embehub.com/img/thumb-hbo.jpg",
        "background": f"{server}https://embehub.com/img/thumb-hbo.jpg",
        "description": "Canal HBO ao vivo.",
        "genres": ["Filmes e Series"],
        "streams": [
            {
                "url": "",
                "title": "HBO",
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
        "id": "skyflix:hbo2",
        "rc": {"token": "c0hIM0JOdmVVRkFWR2poSjExRTI=", "channel": "hbo2"},
        "type": "tv",
        "name": "HBO 2",
        "poster": f"{server}https://embehub.com/img/thumb-hbo2.jpg",
        "background": f"{server}https://embehub.com/img/thumb-hbo2.jpg",
        "description": "Canal HBO 2 ao vivo.",
        "genres": ["Filmes e Series"],
        "streams": [
            {
                "url": "",
                "title": "HBO 2",
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
        "id": "skyflix:hbofamily",
        "rc": {"token": "c0hIM0JOdmVVMUFVRXpoSjExRmk0U3JDaThRPQ==", "channel": "hbofamily"},
        "type": "tv",
        "name": "HBO FAMILY",
        "poster": f"{server}https://embehub.com/img/thumb-hbofamily.jpg",
        "background": f"{server}https://embehub.com/img/thumb-hbofamily.jpg",
        "description": "Canal HBO FAMILY ao vivo.",
        "genres": ["Filmes e Series"],
        "streams": [
            {
                "url": "",
                "title": "HBO FAMILY",
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
        "id": "skyflix:hboplus",
        "rc": {"token": "c0hIM0JOdmZVMU1lRURoSjExRjA3RExZ", "channel": "hboplus"},
        "type": "tv",
        "name": "HBO PLUS",
        "poster": f"{server}https://embehub.com/img/thumb-hboplus.jpg",
        "background": f"{server}https://embehub.com/img/thumb-hboplus.jpg",
        "description": "Canal HBO PLUS ao vivo.",
        "genres": ["Filmes e Series"],
        "streams": [
            {
                "url": "",
                "title": "HBO PLUS",
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
        'id': 'skyflix:hboxtreme',
        "rc": {"token": "c0hIM0JOdmZVRkllRnpoSjExRjg5RFhPaXRnPQ==", "channel": "hboxtreme"},
        'type': 'tv',
        'name': 'HBO XTREME',
        'poster': f"{server}https://embehub.com/img/hboextreme.webp",
        'background': f"{server}https://embehub.com/img/hboextreme.webp",
        'description': 'canal HBO XTREME ao vivo.',
        'genres': ['Filmes e Series'],
        'streams': [
            {
                'url': "",
                'title': "HBO XTREME",
                'behaviorHints': {
                    'notWebReady': True,
                    'proxyHeaders': {
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
        'id': 'skyflix:hbosignature',
        "rc": {"token": "c0hIM0JOdmVVMW9jRWpoSjExRjM2U0RGaHNsbUVUUT0=", "channel": "hbosignature"},
        'type': 'tv',
        'name': 'HBO SIGNATURE',
        'poster': "https://simg.nicepng.com/png/small/233-2333073_hbo-signature-latin-atlansia-hbo-signature-logo-png.png",
        'background': "https://simg.nicepng.com/png/small/233-2333073_hbo-signature-latin-atlansia-hbo-signature-logo-png.png",
        'description': 'canal HBO SIGNATURE ao vivo.',
        'genres': ['Filmes e Series'],
        'streams': [
            {
                'url': "",
                'title': "HBO SIGNATURE",
                'behaviorHints': {
                    'notWebReady': True,
                    'proxyHeaders': {
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
        'id': 'skyflix:hbopop',
        "rc": {"token": "c0hIM0JOdmZWbElkRkRoSjExRjA3emM9", "channel": "hbopop"},
        'type': 'tv',
        'name': 'HBO POP',
        'poster': "https://redecanaistv.ps/player3/imgs-videos/Canais/hbopop.jpg",
        'background': "https://redecanaistv.ps/player3/imgs-videos/Canais/hbopop.jpg",
        'description': 'canal HBO POP ao vivo.',
        'genres': ['Filmes e Series'],
        'streams': [
            {
                'url': "",
                'title': "HBO POP",
                'behaviorHints': {
                    'notWebReady': True,
                    'proxyHeaders': {
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
        'id': 'skyflix:history',
        "rc": {"token": "c0hIM0JOdlVWbEllR2poSjNFMXc3elhT", "channel": "history"},
        'type': 'tv',
        'name': 'HISTORY',
        'poster': f"{server}https://embehub.com/img/thumb-history.jpg",
        'background': f"{server}https://embehub.com/img/thumb-history.jpg",
        'description': 'Canal HISTORY ao vivo.',
        'genres': ['Documentarios'],
        'streams': [
            {
                'url': "",
                'title': "HISTORY",
                'behaviorHints': {
                    'notWebReady': True,
                    'proxyHeaders': {
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
        'id': 'skyflix:history2',
        "rc": {"token": "c0hIM0JOdlVVbE1VRmpoSjNFMXc3elhTMVE9PQ==", "channel": "history2"},
        'type': 'tv',
        'name': 'HISTORY 2',
        'poster': f"{server}https://embehub.com/img/thumb-history2.jpg",
        'background': f"{server}https://embehub.com/img/thumb-history2.jpg",
        'description': 'Canal HISTORY 2 ao vivo.',
        'genres': ['Documentarios'],
        'streams': [
            {
                'url': "",
                'title': "HISTORY 2",
                'behaviorHints': {
                    'notWebReady': True,
                    'proxyHeaders': {
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
        'id': 'skyflix:mtv',
        "rc": {"token": "c0hIM0JOdlZVRnNZRXpoTXdVZz0=", "channel": "mtv"},
        'type': 'tv',
        'name': 'MTV',
        'poster': f"{server}https://embehub.com/img/thumb-mtv.jpg",
        'background': f"{server}https://embehub.com/img/thumb-mtv.jpg",
        'description': 'Canal MTV ao vivo.',
        'genres': ['Variedades'],
        'streams': [
            {
                'url': "",
                'title': "MTV",
                'behaviorHints': {
                    'notWebReady': True,
                    'proxyHeaders': {
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
        'id': 'skyflix:nationalgeographic',
        "rc": {"token": "c0hIM0JOdlVVRllmRVRoUDFFcGo1U2c9", "channel": "natgeo"},
        'type': 'tv',
        'name': 'NATIONAL GEOGRAPHIC',
        'poster': f"{server}https://embehub.com/img/thumb-natgeo.jpg",
        'background': f"{server}https://embehub.com/img/thumb-natgeo.jpg",
        'description': 'Canal NATIONAL GEOGRAPHIC ao vivo.',
        'genres': ['Documentarios'],
        'streams': [
            {
                'url': "",
                'title': "NATIONAL GEOGRAPHIC",
                'behaviorHints': {
                    'notWebReady': True,
                    'proxyHeaders': {
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
        'id': 'skyflix:paramountnetwork',
        "rc": {"token": "c0hIM0JOdmVVMUFmR3poUjFFeGw3U2plaWNrPQ==", "channel": "paramount"},
        'type': 'tv',
        'name': 'PARAMOUNT NETWORK',
        'poster': f"{server}https://embehub.com/img/thumb-paramount.jpg",
        'background': f"{server}https://embehub.com/img/thumb-paramount.jpg",
        'description': 'Canal PARAMOUNT NETWORK ao vivo.',
        'genres': ['Filmes e Series'],
        'streams': [
            {
                'url': "",
                'title': "PARAMOUNT NETWORK",
                'behaviorHints': {
                    'notWebReady': True,
                    'proxyHeaders': {
                        'request': {
                            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            'Origin': "https://redecanaistv.ps/",
                            'Referer': "https://redecanaistv.ps/"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:space',
        "rc": {"token": "c0hIM0JOdmZVbHNaRWpoU3hWOW41UT09", "channel": "space"},
        'type': 'tv',
        'name': 'SPACE',
        'poster': f"{server}https://embehub.com/img/thumb-space.jpg",
        'background': f"{server}https://embehub.com/img/thumb-space.jpg",
        'description': 'Canal SPACE ao vivo.',
        'genres': ['Filmes e Series'],
        'streams': [
            {
                'url': "",
                'title': "SPACE",
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
        'id': 'skyflix:tnt',
        "rc": {"token": "c0hIM0JOdmVVMW9mR3poVjIwbz0=", "channel": "tnt"},
        'type': 'tv',
        'name': 'TNT',
        'poster': f"{server}https://embehub.com/img/thumb-tnt.jpg",
        'background': f"{server}https://embehub.com/img/thumb-tnt.jpg",
        'description': 'Canal TNT ao vivo.',
        'genres': ['Filmes e Series'],
        'streams': [
            {
                'url': "",
                'title': "TNT",
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
        'id': 'skyflix:tntseries',
        "rc": {"token": "c0hIM0JOdmZWRklkRlRoVjIwcDM1VFhDZ3M0PQ==", "channel": "tntseries"},
        'type': 'tv',
        'name': 'TNT SERIES',
        'poster': f"{server}https://redecanaistv.ps/player3/imgs-videos/Canais/tntseries.jpg",
        'background': f"{server}https://redecanaistv.ps/player3/imgs-videos/Canais/tntseries.jpg",
        'description': 'Canal TNT SERIES ao vivo.',
        'genres': ['Filmes e Series'],
        'streams': [
            {
                'url': "",
                'title': "TNT SERIES",
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
        'id': 'skyflix:tntnovelas',
        "rc": {"token": "c0hIM0JOdmZVMU1iRmpoVjIwcHE3ekhPaTl4Zw==", "channel": "tntnovelas"},
        'type': 'tv',
        'name': 'TNT NOVELAS',
        'poster': f"{server}https://redecanaistv.ps/player3/imgs-videos/Canais/tntnovelas.jpg",
        'background': f"{server}https://redecanaistv.ps/player3/imgs-videos/Canais/tntnovelas.jpg",
        'description': 'Canal TNT NOVELAS ao vivo.',
        'genres': ['Filmes e Series'],
        'streams': [
            {
                'url': "",
                'title': "TNT NOVELAS",
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
        'id': 'skyflix:telecineaction',
        "rc": {"token": "c0hIM0JOdmZWRm9WRkRoVjBGSmg0eTdGZ3R4d0Z6anhOZz09", "channel": "telecineaction"},
        'type': 'tv',
        'name': 'TELECINE ACTION',
        'poster': f"{server}https://embehub.com/img/thumb-telecineaction.jpg",
        'background': f"{server}https://embehub.com/img/thumb-telecineaction.jpg",
        'description': 'Canal TELECINE ACTION ao vivo.',
        'genres': ['Filmes e Series'],
        'streams': [
            {
                'url': "",
                'title': "TELECINE ACTION",
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
        'id': 'skyflix:telecinecult',
        "rc": {"token": "c0hIM0JOdmZXRlVaRnpoVjBGSmg0eTdGZ3Q1bUR5VT0=", "channel": "telecinecult"},
        'type': 'tv',
        'name': 'TELECINE CULT',
        'poster': f"{server}https://embehub.com/img/thumb-telecinecult.jpg",
        'background': f"{server}https://embehub.com/img/thumb-telecinecult.jpg",
        'description': 'Canal TELECINE CULT ao vivo.',
        'genres': ['Filmes e Series'],
        'streams': [
            {
                'url': "",
                'title': "TELECINE CULT",
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
        'id': 'skyflix:telecinefun',
        "rc": {"token": "c0hIM0JOdmZVVlFkRVRoVjBGSmg0eTdGZ3R0bURRPT0=", "channel": "telecinefun"},
        'type': 'tv',
        'name': 'TELECINE FUN',
        'poster': f"{server}https://embehub.com/img/thumb-telecinefun.jpg",
        'background': f"{server}https://embehub.com/img/thumb-telecinefun.jpg",
        'description': 'Canal TELECINE FUN ao vivo.',
        'genres': ['Filmes e Series'],
        'streams': [
            {
                'url': "",
                'title': "TELECINE FUN",
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
        'id': 'skyflix:telecinepipoca',
        "rc": {"token": "c0hIM0JOdmZVbG9aR2poVjBGSmg0eTdGZ3MxNkV6NzlPUT09", "channel": "telecinepipoca"},
        'type': 'tv',
        'name': 'TELECINE PIPOCA',
        'poster': f"{server}https://embehub.com/img/thumb-telecinepipoca.jpg",
        'background': f"{server}https://embehub.com/img/thumb-telecinepipoca.jpg",
        'description': 'Canal TELECINE PIPOCA ao vivo.',
        'genres': ['Filmes e Series'],
        'streams': [
            {
                'url': "",
                'title': "TELECINE PIPOCA",
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
        'id': 'skyflix:telecinepremium',
        "rc": {"token": "c0hIM0JOdmVWVlVWRnpoVjBGSmg0eTdGZ3MxaEJqejNMUTA9", "channel": "telecinepremium"},
        'type': 'tv',
        'name': 'TELECINE PREMIUM',
        'poster': f"{server}https://embehub.com/img/thumb-telecinepremium.jpg",
        'background': f"{server}https://embehub.com/img/thumb-telecinepremium.jpg",
        'description': 'Canal TELECINE PREMIUM ao vivo.',
        'genres': ['Filmes e Series'],
        'streams': [
            {
                'url': "",
                'title': "TELECINE PREMIUM",
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
        'id': 'skyflix:telecinetouch',
        "rc": {"token": "c0hIM0JOdmVVMVlhRlRoVjBGSmg0eTdGZ3NsOEZqTDI=", "channel": "telecinetouch"},
        'type': 'tv',
        'name': 'TELECINE TOUCH',
        'poster': f"{server}https://embehub.com/img/thumb-telecinetouch.jpg",
        'background': f"{server}https://embehub.com/img/thumb-telecinetouch.jpg",
        'description': 'Canal TELECINE TOUCH ao vivo.',
        'genres': ['Filmes e Series'],
        'streams': [
            {
                'url': "",
                'title': "TELECINE TOUCH",
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
        'id': 'skyflix:universal',
        "rc": {"token": "c0hIM0JOdmVWRkljRnpoVTIxZHk1VFhZaHRFPQ==", "channel": "universal"},
        'type': 'tv',
        'name': 'UNIVERSAL TV',
        'poster': f"{server}https://embehub.com/img/thumb-universal.jpg",
        'background': f"{server}https://embehub.com/img/thumb-universal.jpg",
        'description': 'Canal UNIVERSAL ao vivo.',
        'genres': ['Filmes e Series'],
        'streams': [
            {
                'url': "",
                'title': "UNIVERSAL TV",
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
        "rc": {"token": "c0hIM0JOdmZVVm9lRlRoQzNGQmg3U2JU", "channel": "cinemax"},
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
        "rc": {"token": "c0hIM0JOdlVWbFVlRkRoQzJsTmg1RDdJZ3RObkVURHk=", "channel": "comedycentral"},        
        "type": "tv",
        "name": "COMEDY CENTRAL",
        "poster": f"{server}https://embehub.com/img/thumb-comedycentral.jpg",
        "background": f"{server}https://embehub.com/img/thumb-comedycentral.jpg",
        "description": "Canal COMEDY CENTRAL ao vivo.",
        "genres": ["Variedades"],
        "streams": [
            {
                "url": "",
                "title": "COMEDY CENTRAL",
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
        "id": "skyflix:sony",
        "rc": {"token": "c0hIM0JOdmZXVkFiRmpoUzJsQjk=", "channel": "sony"},
        "type": "tv",
        "name": "SONY CHANNEL",
        "poster": f"{server}https://embehub.com/img/thumb-sony.jpg",
        "background": f"{server}https://embehub.com/img/thumb-sony.jpg",
        "description": "SONY CHANNEL ao vivo.",
        "genres": ["Filmes e Series"],
        "streams": [
            {
                "url": "",
                "title": "SONY CHANNEL",
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
        "id": "skyflix:sonymovies",
        "rc": {"token": "c0hIM0JOdmZXRm9ZR3poUzJsQjk3U2pkanRoZw==", "channel": "sonymovies"},
        "type": "tv",
        "name": "SONY MOVIES",
        "poster": f"{server}https://redecanaistv.ps/player3/imgs-videos/Canais/sonymovies.jpg",
        "background": f"{server}https://redecanaistv.ps/player3/imgs-videos/Canais/sonymovies.jpg",
        "description": "SONY MOVIES ao vivo.",
        "genres": ["Filmes e Series"],
        "streams": [
            {
                "url": "",
                "title": "SONY MOVIES",
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
        "id": "skyflix:starchannel",
        "rc": {"token": "c0hIM0JOdmVVRllVRWpoU3dWOTI0eS9LaWROMkR3PT0=", "channel": "starchannel"},
        "type": "tv",
        "name": "STAR CHANNEL",
        "poster": f"{server}https://embehub.com/img/thumb-starchannel.jpg",
        "background": f"{server}https://embehub.com/img/thumb-starchannel.jpg",
        "description": "STAR CHANNEL ao vivo.",
        "genres": ["Filmes e Series"],
        "streams": [
            {
                "url": "",
                "title": "STAR CHANNEL",
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
        "id": "skyflix:warnertv",
        "rc": {"token": "c0hIM0JOdmZWbFlZRlRoVzFFeHE1VFU9", "channel": "warner"},
        "type": "tv",
        "name": "WARNER TV",
        "poster": f"{server}https://embehub.com/img/thumb-warner.jpg",
        "background": f"{server}https://embehub.com/img/thumb-warner.jpg",
        "description": "canal WARNER TV ao vivo.",
        "genres": ["Filmes e Series"],
        "streams": [
            {
                "url": "",
                "title": "WARNER TV",
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
        "id": "skyflix:aie",
        "rc": {"token": "c0hIM0JOdmVVbFliRWpoQTNGcz0=", "channel": "aie"},
        "type": "tv",
        "name": "A&E",
        "poster": f"{server}https://embehub.com/img/A&E_Network_logo.png",
        "background": f"{server}https://embehub.com/img/A&E_Network_logo.png",
        "description": "canal A&E ao vivo.",
        "genres": ["Filmes e Series"],
        "streams": [
            {
                "url": "",
                "title": "A&E",
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
        "id": "skyflix:investigacao",
        "rc": {"token": "c0hIM0JOdlZXVmNZR2poSTIwaGg4elBDZ054d0FqNzZNUlBnZEIvdjVNZz0=", "channel": "investigacaodiscovery"},
        "type": "tv",
        "name": "INVESTIGAÇÃO DISCOVERY",
        "poster": f"{server}https://embehub.com/img/iddiscovery.jpeg",
        "background": f"{server}https://embehub.com/img/iddiscovery.jpeg",
        "description": "canal INVESTIGAÇÃO DISCOVERY ao vivo.",
        "genres": ["Documentarios"],
        "streams": [
            {
                "url": "",
                "title": "INVESTIGAÇÃO DISCOVERY",
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
        "id": "skyflix:tlc",
        "rc": {"token": "c0hIM0JOdmFVMU1aRVRoVjJWMD0=", "channel": "tlc"},
        "type": "tv",
        "name": "TLC",
        "poster": f"{server}https://embehub.com/img/discoverytlc.png",
        "background": f"{server}https://embehub.com/img/discoverytlc.png",
        "description": "canal TLC ao vivo.",
        "genres": ["Documentarios"],
        "streams": [
            {
                "url": "",
                "title": "TLC",
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
        "id": "skyflix:megapix",
        "rc": {"token": "c0hIM0JOdmZVVkVaR3poTTBGbGw4QzdU", "channel": "megapix"},
        "type": "tv",
        "name": "MEGAPIX",
        "poster": f"{server}https://embehub.com/img/megapix.jpg",
        "background": f"{server}https://embehub.com/img/megapix.jpg",
        "description": "canal MEGAPIX ao vivo.",
        "genres": ["Filmes e Series"],
        "streams": [
            {
                "url": "",
                "title": "MEGAPIX",
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
        "id": "skyflix:studiouniversal",
        "rc": {"token": "c0hIM0JOdmZVMU1lRnpoU3dVdGc2U2plaWRSbEJpUHRPUXc9", "channel": "studiouniversal"},
        "type": "tv",
        "name": "STUDIO UNIVERSAL",
        "poster": f"{server}https://embehub.com/img/universalstudios.png",
        "background": f"{server}https://embehub.com/img/universalstudios.png",
        "description": "canal STUDIO UNIVERSAL ao vivo.",
        "genres": ["Filmes e Series"],
        "streams": [
            {
                "url": "",
                "title": "STUDIO UNIVERSAL",
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
        "id": "skyflix:lifetime",
        "rc": {"token": "c0hIM0JOdmZWVlVZR2poTjNGaGg5QzdHZ2c9PQ==", "channel": "lifetime"},
        "type": "tv",
        "name": "LIFETIME",
        "poster": f"{server}https://i.ibb.co/jGXbx1x/lifetime.jpg",
        "background": f"{server}https://i.ibb.co/jGXbx1x/lifetime.jpg",
        "description": "canal LIFETIME ao vivo.",
        "genres": ["Filmes e Series"],
        "streams": [
            {
                "url": "",
                "title": "LIFETIME",
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
        "id": "skyflix:cinecanal",
        "rc": {"token": "c0hIM0JOdmVVMU1kR3poQzNGQmg0eWJGaHRFPQ==", "channel": "cinecanal"},
        "type": "tv",
        "name": "CINE CANAL",
        "poster": f"{server}https://seeklogo.com/images/C/Cinecanal-logo-C68A0CF747-seeklogo.com.png",
        "background": f"{server}https://seeklogo.com/images/C/Cinecanal-logo-C68A0CF747-seeklogo.com.png",
        "description": "CINE CANAL ao vivo.",
        "genres": ["Filmes e Series"],
        "streams": [
            {
                "url": "",
                "title": "CINE CANAL",
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
        "id": "skyflix:eentertainment",
        "rc": {"token": "c0hIM0JOdlZWVllmRnpoQzFGQmw3Q0k9", "channel": "canale"},
        "type": "tv",
        "name": "!E",
        "poster": f"{server}https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/E%21_Logo.svg/1200px-E%21_Logo.svg.png",
        "background": f"{server}https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/E%21_Logo.svg/1200px-E%21_Logo.svg.png",
        "description": "canal !E ao vivo.",
        "genres": ["Variedades"],
        "streams": [
            {
                "url": "",
                "title": "!E",
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
        "id": "skyflix:bandsports",
        "rc": {"token": "c0hIM0JOdmNXRmNiRmpoRDFGQmc4emZFbGNsZw==", "channel": "bandsports"}, 
        "type": "tv",
        "name": "BANDSPORTS",
        "poster": f"{server}https://embehub.com/img/thumb-bandsports.jpg",
        "background": f"{server}https://embehub.com/img/thumb-bandsports.jpg",
        "description": "canal BANDSPORTS ao vivo.",
        "genres": ["Esportes"],
        "streams": [
            {
                "url": "",
                "title": "BANDSPORTS",
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
        "id": "skyflix:espn",
        "rc": {"token": "c0hIM0JOdmZVbFViRURoRXhrNXE=", "channel": "espn"}, 
        "type": "tv",
        "name": "ESPN",
        "poster": f"{server}https://embehub.com/img/thumb-espn.jpg",
        "background": f"{server}https://embehub.com/img/thumb-espn.jpg",
        "description": "canal ESPN ao vivo.",
        "genres": ["Esportes"],
        "streams": [
            {
                "url": "",
                "title": "ESPN",
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
        "id": "skyflix:espn2",
        "rc": {"token": "c0hIM0JOdmZVbG9iRWpoRXhrNXFzZz09", "channel": "espn2"}, 
        "type": "tv",
        "name": "ESPN 2",
        "poster": f"{server}https://embehub.com/img/thumb-espn2.jpg",
        "background": f"{server}https://embehub.com/img/thumb-espn2.jpg",
        "description": "canal ESPN 2 ao vivo.",
        "genres": ["Esportes"],
        "streams": [
            {
                "url": "",
                "title": "ESPN 2",
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
        "id": "skyflix:espn3",
        "rc": {"token": "c0hIM0JOdmNVbG9jRkRoRXhrNXFzdz09", "channel": "espn3"},
        "type": "tv",
        "name": "ESPN 3",
        "poster": f"{server}https://embehub.com/img/thumb-espn3.jpg",
        "background": f"{server}https://embehub.com/img/thumb-espn3.jpg",
        "description": "canal ESPN 3 ao vivo.",
        "genres": ["Esportes"],
        "streams": [
            {
                "url": "",
                "title": "ESPN 3",
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
        "id": "skyflix:espn4",
        "rc": {"token": "c0hIM0JOdmNWbG9lRWpoRXhrNXF0QT09", "channel": "espn4"},
        "type": "tv",
        "name": "ESPN 4",
        "poster": f"{server}https://embehub.com/img/thumb-espn4.jpg",
        "background": f"{server}https://embehub.com/img/thumb-espn4.jpg",
        "description": "canal ESPN 4 ao vivo.",
        "genres": ["Esportes"],
        "streams": [
            {
                "url": "",
                "title": "ESPN 4",
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
        "id": "skyflix:espn5",
        "rc": {"token": "c0hIM0JOdmNWMUFaRXpoRXhrNXF0UT09", "channel": "espn5"},
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
                            "Origin": "https://redecanaistv.ps",
                            "Referer": "https://redecanaistv.ps/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:espn6",
        "rc": {"token": "c0hIM0JOdmNVVlFlR2poRXhrNXF0Zz09", "channel": "espn6"},
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
                            "Origin": "https://redecanaistv.ps",
                            "Referer": "https://redecanaistv.ps/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:sportv",
        "rc": {"token": "c0hIM0JOdmVVVm9hR2poU3hWRjI5REdh", "channel": "sportv1"},
        "type": "tv",
        "name": "SPORTV",
        "poster": f"{server}https://embehub.com/img/thumb-sportv1.jpg",
        "background": f"{server}https://embehub.com/img/thumb-sportv1.jpg",
        "description": "canal SPORTV ao vivo.",
        "genres": ["Esportes"],
        "streams": [
            {
                "url": "",
                "title": "SPORTV",
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
        "id": "skyflix:sportv2",
        "rc": {"token": "c0hIM0JOdmZVVkVhRWpoU3hWRjI5REda", "channel": "sportv2"},
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
                            "Origin": "https://redecanaistv.ps",
                            "Referer": "https://redecanaistv.ps/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:sportv3",
        "rc": {"token": "c0hIM0JOdmNXRnNaRVRoU3hWRjI5REdZ", "channel": "sportv3"},
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
                            "Origin": "https://redecanaistv.ps",
                            "Referer": "https://redecanaistv.ps/"
                        }
                    }
                }
            }
        ]
    },
    {
        "id": "skyflix:premiereclubes",
        "rc": {"token": "c0hIM0JOdmRWRlFWRlRoUngxdHA2U0xaZ3Q1L0ZqUDdLdz09", "channel": "premiereclubes"},
        "type": "tv",
        "name": "PREMIERE CLUBES",
        "poster": f"{server}https://embehub.com/img/thumb-premiereclubes.jpg",
        "background": f"{server}https://embehub.com/img/thumb-premiereclubes.jpg",
        "description": "canal PREMIERE CLUBES ao vivo.",
        "genres": ["Esportes"],
        "streams": [
            {
                "url": "",
                "title": "PREMIERE CLUBES",
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
        "id": "skyflix:premiere2",
        "rc": {"token": "c0hIM0JOclVWRm9aR3poUngxdHA2U0xaZ284PQ==", "channel": "premiere2"}, 
        "type": "tv",
        "name": "PREMIERE 2",
        "poster": f"{server}https://embehub.com/img/thumb-premiere2.jpg",
        "background": f"{server}https://embehub.com/img/thumb-premiere2.jpg",
        "description": "canal PREMIERE 2 ao vivo.",
        "genres": ["Esportes"],
        "streams": [
            {
                "url": "",
                "title": "PREMIERE 2",
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
        "id": "skyflix:premiere3",
        "rc": {"token": "c0hIM0JOclVVRmNZRURoUngxdHA2U0xaZ280PQ==", "channel": "premiere3"},
        "type": "tv",
        "name": "PREMIERE 3",
        "poster": f"{server}https://embehub.com/img/thumb-premiere3.jpg",
        "background": f"{server}https://embehub.com/img/thumb-premiere3.jpg",
        "description": "canal PREMIERE 3 ao vivo.",
        "genres": ["Esportes"],
        "streams": [
            {
                "url": "",
                "title": "PREMIERE 3",
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
        "id": "skyflix:premiere4",
        "rc": {"token": "c0hIM0JOclVVRkVlRmpoUngxdHA2U0xaZ29rPQ==", "channel": "premiere4"},
        "type": "tv",
        "name": "PREMIERE 4",
        "poster": f"{server}https://embehub.com/img/thumb-premiere4.jpg",
        "background": f"{server}https://embehub.com/img/thumb-premiere4.jpg",
        "description": "canal PREMIERE 4 ao vivo.",
        "genres": ["Esportes"],
        "streams": [
            {
                "url": "",
                "title": "PREMIERE 4",
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
        "id": "skyflix:premiere5",
        "rc": {"token": "c0hIM0JOclVXVklWR2poUngxdHA2U0xaZ29nPQ==", "channel": "premiere5"},
        "type": "tv",
        "name": "PREMIERE 5",
        "poster": f"{server}https://embehub.com/img/thumb-premiere5.jpg",
        "background": f"{server}https://embehub.com/img/thumb-premiere5.jpg",
        "description": "canal PREMIERE 5 ao vivo.",
        "genres": ["Esportes"],
        "streams": [
            {
                "url": "",
                "title": "PREMIERE 5",
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
        "id": "skyflix:premiere6",
        "type": "tv",
        "name": "PREMIERE 6",
        "poster": f"{server}https://embehub.com/img/thumb-premiere6.jpg",
        "background": f"{server}https://embehub.com/img/thumb-premiere6.jpg",
        "description": "canal PREMIERE 6 ao vivo.",
        "genres": ["Esportes"],
        "streams": [
            {
                "url": "",
                "title": "PREMIERE 6",
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
        "id": "skyflix:premiere7",
        "rc": {"token": "c0hIM0JOclVXVnNhRmpoUngxdHA2U0xaZ29vPQ==", "channel": "premiere7"},        
        "type": "tv",
        "name": "PREMIERE 7",
        "poster": f"{server}https://embehub.com/img/thumb-premiere7.jpg",
        "background": f"{server}https://embehub.com/img/thumb-premiere7.jpg",
        "description": "canal PREMIERE 7 ao vivo.",
        "genres": ["Esportes"],
        "streams": [
            {
                "url": "",
                "title": "PREMIERE 7",
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
        "rc": {"token": "c0hIM0JOdlZWbG9VRkRoQzFFeHc3eWpG", "channel": "cartoon"},
        'type': 'tv',
        'name': 'CARTOON NETWORK',
        'poster': f"{server}https://embehub.com/img/thumb-cartoon.jpg",
        'background': f"{server}https://embehub.com/img/thumb-cartoon.jpg",
        'description': 'canal CARTOON NETWORK ao vivo.',
        'genres': ['Infantil'],
        'streams': [
            {
                "url": "",
                "title": "CARTOON NETWORK",
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
        'id': 'skyflix:discoverykids',
        "rc": {"token": "c0hIM0JOdmFXVm9WRWpoRjNFMW43ekhPbGNSNENqWHQ=", "channel": "discoverykids"},
        'type': 'tv',
        'name': 'DISCOVERY KIDS',
        'poster': f"{server}https://embehub.com/img/thumb-discoverykids.jpg",
        'background': f"{server}https://embehub.com/img/thumb-discoverykids.jpg",
        'description': 'canal DISCOVERY KIDS ao vivo.',
        'genres': ['Infantil'],
        'streams': [
            {
                "url": "",
                "title": "DISCOVERY KIDS",
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
        'id': 'skyflix:disney',
        "rc": {"token": "c0hIM0JOdlZWVm9ZR3poRjNFMXE1VDQ9", "channel": "disney"},
        'type': 'tv',
        'name': 'DISNEY CHANNEL',
        'poster': f"{server}https://embehub.com/img/thumb-disney.jpg",
        'background': f"{server}https://embehub.com/img/thumb-disney.jpg",
        'description': 'canal DISNEY CHANNEL ao vivo.',
        'genres': ['Infantil'],
        'streams': [
            {
                "url": "",
                "title": "DISNEY CHANNEL",
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
        'id': 'skyflix:nick',
        "rc": {"token": "c0hIM0JOdmFXRkViRXpoUDNGMXY=", "channel": "nick"},
        'type': 'tv',
        'name': 'NICKELODEON',
        'poster': f"{server}https://embehub.com/img/thumb-nick.jpg",
        'background': f"{server}https://embehub.com/img/thumb-nick.jpg",
        'description': 'canal NICKELODEON ao vivo.',
        'genres': ['Infantil'],
        'streams': [
            {
                "url": "",
                "title": "NICKELODEON",
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
        'id': 'skyflix:nickjr',
        "rc": {"token": "c0hIM0JOdmFWMUViRlRoUDNGMXY2alU9", "channel": "nickjr"},
        'type': 'tv',
        'name': 'NICK JR.',
        'poster': f"{server}https://embehub.com/img/thumb-nickjr.jpg",
        'background': f"{server}https://embehub.com/img/thumb-nickjr.jpg",
        'description': 'canal NICK JR. ao vivo.',
        'genres': ['Infantil'],
        'streams': [
            {
                "url": "",
                "title": "NICK JR.",
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
        'id': 'skyflix:cartoonito',
        "rc": {"token": "c0hIM0JOdlZVMW9iR2poQzFFeHc3eWpGanNsOA==", "channel": "cartoonito"},
        'type': 'tv',
        'name': 'CARTOONITO',
        'poster': f"{server}https://embehub.com/img/thumb-cartoonito.jpg",
        'background': f"{server}https://embehub.com/img/thumb-cartoonito.jpg",
        'description': 'canal CARTOONITO ao vivo.',
        'genres': ['Infantil'],
        'streams': [
            {
                "url": "",
                "title": "CARTOONITO",
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
        'id': 'skyflix:gloobinho',
        "rc": {"token": "c0hIM0JOdlVWRk1aRkRoRzJWRnI0aTdGajlJPQ==", "channel": "gloobinho"},
        'type': 'tv',
        'name': 'GLOOBINHO',
        'poster': f"{server}https://embehub.com/img/globinho.png",
        'background': f"{server}https://embehub.com/img/globinho.png",
        'description': 'canal GLOOBINHO ao vivo.',
        'genres': ['Infantil'],
        'streams': [
            {
                "url": "",
                "title": "GLOOBINHO",
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
        'id': 'skyflix:gloob',
        "rc": {"token": "c0hIM0JOdmFXRklhRmpoRzJWRnI0Zz09", "channel": "gloob"},
        'type': 'tv',
        'name': 'GLOOB',
        'poster': f"{server}https://embehub.com/img/gloob.png",
        'background': f"{server}https://embehub.com/img/gloob.png",
        'description': 'canal GLOOB ao vivo.',
        'genres': ['Infantil'],
        'streams': [
            {
                "url": "",
                "title": "GLOOB",
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
        'id': 'skyflix:bandnews',
        "rc": {"token": "c0hIM0JOdlZVRkFlR3poRDFGQmc3aUxjbEE9PQ==", "channel": "bandnews"},
        'type': 'tv',
        'name': 'BAND NEWS',
        'poster': f"{server}https://embehub.com/img/thumb-bandnews.jpg",
        'background': f"{server}https://embehub.com/img/thumb-bandnews.jpg",
        'description': 'canal BAND NEWS ao vivo.',
        'genres': ['Noticias'],
        'streams': [
            {
                "url": "",
                "title": "BAND NEWS",
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
        "rc": {"token": "c0hIM0JOdlZVRlFaRmpoVDBGMXI4aVBGZ3NwZw==", "channel": "recordnews"},
        'type': 'tv',
        'name': 'RECORD NEWS',
        'poster': f"{server}https://embehub.com/img/recordnews.png",
        'background': f"{server}https://embehub.com/img/recordnews.png",
        'description': 'canal RECORD NEWS ao vivo.',
        'genres': ['Noticias'],
        'streams': [
            {
                "url": "",
                "title": "RECORD NEWS",
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
        'id': 'skyflix:globonews',
        "rc": {"token": "c0hIM0JOdmFWRmNaRnpoRzJWRm03eW5Pa000PQ==", "channel": "globonews"},
        'type': 'tv',
        'name': 'GLOBO NEWS',
        'poster': f"{server}https://embehub.com/imagens/globonews.png",
        'background': f"{server}https://embehub.com/imagens/globonews.png",
        'description': 'canal GLOBO NEWS ao vivo.',
        'genres': ['Noticias'],
        'streams': [
            {
                "url": "",
                "title": "GLOBO NEWS",
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
        "rc": {"token": "c0hIM0JOdmJWMUliRURoRDExdzJ0U1k9", "channel": "bbb25a"},
        'type': 'tv',
        'name': 'BBB 25 CAM 1',
        'poster': f"{server}https://embehub.com/img/bbb25.png",
        'background': f"{server}https://embehub.com/img/bbb25.png",
        'description': 'canal BBB 25 CAM 1 ao vivo.',
        'genres': ['Variedades'],
        'streams': [
            {
                "url": "",
                "title": "BBB 25 CAM 1",
                "behaviorHints": {
                    "notWebReady": True,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                            "Origin": "https://redecanaistv.ps",
                            "Referer": "https://redecanaistv.ps"
                        }
                    }
                }
            }
        ]
    },
    {
        'id': 'skyflix:bbb25cam2',
        "rc": {"token": "c0hIM0JOdlZWVklVRmpoRDExdzJ0U1U9", "channel": "bbb25b"},
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
                            "Origin": "https://redecanaistv.ps",
                            "Referer": "https://redecanaistv.ps"
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
    },
    {
        'id': 'skyflix:nossofutebol',
        "rc": {"token": "c0hIM0JOdmFXRkFkRWpoUDJrMTM3eUhlazloeEREMD0=", "channel": "nossofutebol"},
        'type': 'tv',
        'name': 'NOSSO FUTEBOL',
        'poster': f"{server}https://redecanaistv.ps/player3/imgs-videos/Canais/nossofutebol.jpg",
        'background': f"{server}https://redecanaistv.ps/player3/imgs-videos/Canais/nossofutebol.jpg",
        'description': 'canal NOSSO FUTEBOL ao vivo.',
        'genres': ['Esportes'],
        'streams': [
            {
                "url": "",
                "title": "NOSSO FUTEBOL",
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
    }                                                                                                                              
    ]
    return canais

# def get_rc(channel,token):
#     stream = ''
#     try:
#         headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0'}
#         page = f'https://oneplayhd.com/rcproxy/rcproxy2.php?channel={quote(channel)}&token={quote(token)}'         
#         r = requests.get(page,headers=headers,allow_redirects=False,timeout=6)
#         if r.status_code in [301, 302]:
#             stream = r.headers.get("Location")
#             if stream.startswith('//'):
#                 stream = 'https:' + stream               
#     except:
#         pass
#     return stream

def unfuck_rc(html):
    try:
        secret = re.findall(r'replace.+?-\s*(\d+)', html)[0]
        soup = BeautifulSoup(html, "html.parser")
        script_content = soup.find('script').string
        base64_values = []
        for line in script_content.splitlines():
            try:
                line = line.split('""')[1]
            except:
                pass
            if '"' in line:
                bases_64 = re.findall(r'"(.*?)"', line)
                if bases_64:
                    for base64_value in bases_64:
                        base64_values.append(str(base64_value))
        nzB = ""
        for value in base64_values:
            decoded = base64.b64decode(value).decode('utf-8')
            number = int(''.join(filter(str.isdigit, decoded)))
            nzB += chr(number - int(secret))
        if nzB:
            html = nzB
    except:
        pass
    return html 

def get_token(channel): 
    token = ''   
    url = f'https://redecanaistv.ps/player3/ch.php?categoria=live&canal={channel}'
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0',
                'Origin': 'https://redecanaistv.ps',
                'Referer': 'https://redecanaistv.ps/',
                'accept-language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin'}
    cookie = {'modalVisited':'true'}
    r = requests.get(url,headers=headers,cookies=cookie)
    if r.status_code == 200:
        src = r.text
        html = unfuck_rc(src)
        try:
            token = re.findall(r"'rctoken':'(.*?)'", html)[-1]
        except:
            pass
    return token

def get_rc(channel,token):
    stream = ''
    try:
        # fix token random
        try:
            token = get_token(channel)
        except:
            pass
        # access channel
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0',
                'Origin': 'https://redecanaistv.ps',
                'Referer': 'https://redecanaistv.ps/',
                'accept-language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'x-requested-with': 'XMLHttpRequest'}
        page = f'https://redecanaistv.ps/player3/chforms.api?canal={channel}'
        cookie = {'modalVisited':'true'}
        data = {'rctoken': token}
        r = requests.post(page,headers=headers,cookies=cookie,data=data,timeout=6)
        if r.status_code == 200:
            stream = re.findall(r'src:\s*"(.*?)"', r.text)[-1]
            if stream.startswith('//'):
                stream = 'https:' + stream
            # fix stream
            stream = stream.replace('\n', '').replace(' ', '')
        else:
            stream = 'code_' + str(r.status_code)
    except:
        pass
    return stream



# print(get_rc('bobosp', 'c0hIM0JOdmVXVk1VRmpoRDJseHI4emM9'))
