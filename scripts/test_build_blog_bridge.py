import tempfile
import unittest
from pathlib import Path

from build_blog_bridge import bridge_html, destination, plan_bridge, rewrite_feed_links


class BlogBridgeTest(unittest.TestCase):
    def test_canonical_aliases_escape_and_special_pages(self):
        with tempfile.TemporaryDirectory() as tmp:
            public = Path(tmp)
            for name in ('index.html', '별칭/index.html'):
                path = public / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('<link rel="canonical" href="https://tech.mdeeno.com/posts/한글/&quot;제목&quot;/">기존 본문')
            (public / '404.html').write_text('old 404')
            (public / 'offline.html').write_text('old offline')
            plans = {str(path.relative_to(public)): (text, target) for path, text, target in plan_bridge(public)}
            expected = 'https://mdeeno.com/blog/posts/%ED%95%9C%EA%B8%80/%22%EC%A0%9C%EB%AA%A9%22'
            self.assertEqual(plans['별칭/index.html'][1], expected)
            self.assertIn('content="0; url=', plans['별칭/index.html'][0])
            self.assertNotIn('기존 본문', plans['별칭/index.html'][0])
            self.assertEqual(plans['별칭/index.html'][0].count('<script>'), 1)
            self.assertLess(plans['별칭/index.html'][0].index('<script>'), plans['별칭/index.html'][0].index('http-equiv'))
            self.assertIsNone(plans['404.html'][1])
            self.assertNotIn('http-equiv', plans['404.html'][0])
            self.assertEqual(plans['offline.html'][1], 'https://mdeeno.com/blog')
            self.assertIn('&amp;', bridge_html('https://mdeeno.com/blog?a=1&b=2'))
            # dry-run 계획 생성은 원본 출력도 수정하지 않는다.
            self.assertIn('기존 본문', (public / 'index.html').read_text())
            (public / 'index.html').write_text(plans['index.html'][0])
            rebuilt = {path.name: target for path, _, target in plan_bridge(public)}
            self.assertEqual(rebuilt['index.html'], expected)

    def test_unsafe_canonical_rejected_and_feed_links_preserved(self):
        for url in ('http://tech.mdeeno.com/a', 'https://evil.example/a',
                    'https://mdeeno.com/member', 'https://tech.mdeeno.com/a/%2e%2e/b',
                    'https://tech.mdeeno.com/a%5cb', 'https://tech.mdeeno.com/a%00',
                    'https://user@tech.mdeeno.com/a', 'https://tech.mdeeno.com:443/a'):
            with self.subTest(url=url), self.assertRaises(ValueError):
                destination(url)
        xml = ('<link>https://tech.mdeeno.com/posts/한글/</link>'
               '<guid>https://tech.mdeeno.com/index.xml</guid>'
               '<description>https://tech.mdeeno.com/images/chart.webp</description>')
        output = rewrite_feed_links(xml)
        self.assertIn('<link>https://mdeeno.com/blog/posts/%ED%95%9C%EA%B8%80</link>', output)
        self.assertIn('https://mdeeno.com/blog/index.xml', output)
        self.assertIn('https://tech.mdeeno.com/images/chart.webp', output)


if __name__ == '__main__':
    unittest.main()
