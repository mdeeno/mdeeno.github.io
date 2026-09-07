import datetime as dt
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from check_blog_release import check_new_publication, check_post, check_public_terminology


class TerminologyGateTest(unittest.TestCase):
    def test_legacy_noindex_and_complex_are_checked_without_rewriting_legal_terms(self):
        with tempfile.TemporaryDirectory() as tmp:
            blog = Path(tmp)
            posts = blog / "content" / "posts"
            complex_dir = blog / "content" / "complex"
            posts.mkdir(parents=True)
            complex_dir.mkdir()
            legacy = posts / "legacy.md"
            complex_page = complex_dir / "complex.md"
            legacy.write_text(
                "---\ndraft: false\nrobotsNoIndex: true\n---\n조합원 **부담금**",
                encoding="utf-8",
            )
            complex_page.write_text("---\n  title: 단지\n---\n추가부담금", encoding="utf-8")
            self.assertEqual(len(check_public_terminology(blog)), 2)
            legacy.write_text(
                "---\ndraft: false\nrobotsNoIndex: true\n---\n"
                "조합원 분담금, 재건축부담금, 개발부담금, 재초환 부담금, "
                "법령상 “개략적인 부담금”, 추가 준비 자금\n"
                "[분담금](/posts/추가부담금/) <a href='/추가부담금/'>분담금</a>",
                encoding="utf-8",
            )
            complex_page.write_text("---\n  draft: true\n---\n추가부담금", encoding="utf-8")
            self.assertEqual(check_public_terminology(blog), [])

    def test_weekly_seoul_sources_pass_the_same_release_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            post = Path(tmp) / "weekly.md"
            post.write_text(
                "---\ntitle: 정비사업 위클리\ndate: 2026-09-11\n"
                "description: " + "공식 발표와 조합원 확인 사항을 구분합니다. " * 3 + "\n"
                "tags: [재건축]\nsourceBacked: true\nreviewStatus: approved\n"
                "contentBriefId: weekly-test\nprimaryKeyword: 정비사업\n"
                "searchIntent: 정보\nfunnelGoal: 진단\nsources:\n"
                "  - https://www.seoul.go.kr/news/news_report.do#view/1\n"
                "  - https://www.seoul.go.kr/news/news_report.do#view/2\n---\n"
                "## 핵심 답변\n" + "시나리오 추정이며 실제 조합 자료를 확인하세요. " * 100
                + "\n## 공식 발표\n/posts/guide/ /calculators/calc_interest/ /complex/\n"
                "## 확인 사항\n<div class='blog-cta-box'>"
                "utm_source=blog&utm_medium=blog_cta&utm_campaign=source_backed"
                "&utm_content=weekly-test</div>\n",
                encoding="utf-8",
            )
            self.assertEqual(check_post(post), ([], []))


class WeeklyLaunchGateTest(unittest.TestCase):
    def test_launch_exception_is_single_use_and_does_not_shorten_next_cooldown(self):
        with tempfile.TemporaryDirectory() as tmp, patch("check_blog_release.dt.datetime") as clock:
            blog = Path(tmp)
            posts = blog / "content" / "posts"
            posts.mkdir(parents=True)
            clock.now.return_value.date.return_value = dt.date(2026, 9, 7)

            def write_post(name, date, brief="evergreen", weekly=False, status="approved"):
                path = posts / name
                path.write_text(
                    f"---\ndate: {date}\nsourceBacked: true\nreviewStatus: {status}\n"
                    f"draft: false\nrobotsNoIndex: false\ncontentBriefId: {brief}\n"
                    f"weeklyBriefing: {str(weekly).lower()}\n---\n본문\n",
                    encoding="utf-8",
                )
                return path

            write_post("previous.md", "2026-09-04")
            launch = write_post("launch.md", "2026-09-07", "weekly-2026-w37", True)
            self.assertEqual(check_new_publication(blog, [launch]), [])
            for date, brief, weekly, status in (
                ("2026-09-07", "other", True, "approved"),
                ("2026-09-07", "weekly-2026-w37", False, "approved"),
                ("2026-09-08", "weekly-2026-w37", True, "approved"),
                ("2026-09-07", "weekly-2026-w37", True, "pending"),
            ):
                with self.subTest(date=date, brief=brief, weekly=weekly, status=status):
                    write_post("launch.md", date, brief, weekly, status)
                    self.assertTrue(check_new_publication(blog, [launch]))
            write_post("launch.md", "2026-09-07", "weekly-2026-w37", True)
            clock.now.return_value.date.return_value = dt.date(2026, 9, 8)
            self.assertTrue(check_new_publication(blog, [launch]))
            clock.now.return_value.date.return_value = dt.date(2026, 9, 7)
            second = write_post("second.md", "2026-09-07", "weekly-2026-w37", True)
            self.assertTrue(check_new_publication(blog, [launch, second]))
            self.assertTrue(check_new_publication(blog, [second]))
            write_post("second.md", "2026-09-13", "weekly-2026-w38", True)
            self.assertTrue(check_new_publication(blog, [second]))
            write_post("second.md", "2026-09-14", "weekly-2026-w38", True)
            self.assertEqual(check_new_publication(blog, [second]), [])


if __name__ == "__main__":
    unittest.main()
