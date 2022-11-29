import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    links = corpus[page]
    if not corpus:  return {p: 1/len(corpus) for p in corpus}
    return {p: (damping_factor * 1/len(links) + (1-damping_factor)/len(corpus) if p in links else (1-damping_factor)/len(corpus)) for p in corpus}



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    sample_page_rank = {p: 0 for p in corpus}
    cur_page = random.choice(list(corpus))
    for _ in range(n):
        probabilities = transition_model(corpus, cur_page, damping_factor)
        population = []
        weight = []
        for k,v in probabilities.items():
            population.append(k)
            weight.append(v)
        cur_page = random.choices(population, weight)[0]
        sample_page_rank[cur_page] += 1

    return {k: v/n for k,v in sample_page_rank.items()}


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    BASE = (1 - damping_factor)/N
    iter_page_rank = {p: 1/N for p in corpus}
    big_changes = 1
    while big_changes:
        big_changes = 0
        for page in corpus:
            references = set()
            for k, v in corpus.items():
                if page in v:
                    references.add((k, len(v)))
                if not v:
                    references.add((k, N))
            factor = damping_factor * (sum([iter_page_rank[x[0]]/x[1] for x in references]))
            old = iter_page_rank[page]
            new = BASE + factor
            iter_page_rank[page] = new
            if abs(old-new) > 0.001:
                big_changes += 1
    return iter_page_rank





if __name__ == "__main__":
    main()
