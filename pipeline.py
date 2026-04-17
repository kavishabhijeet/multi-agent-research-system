from agents import build_reader_agent,build_serach_agent,writer_chain,critic_chain

# Step 1 Searcg agent
def run_research_pipeline(topic : str) -> dict:
    state = {}
    print("Step 1 - Agent is working now")

    search_agent = build_serach_agent()
    search_result = search_agent.invoke({
        "messages" : [("user",f"Find recent, reliable,detailed information about: {topic}")]
    })
    
    state["search_results"] = search_result['messages'][-1].content

    print("\n search_result ",state["search_results"])

    # Step 2 Reader agent
    print("Step 2 -Reader Agent is scraping from the resources....")
    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages" :[("user",
                      f"Based on the following search results about{'topic'},"
                      f"Pick the most relevent URL and scrape it deeper content.\n\n"
                      f"Search Results: \n{state['search_results'][:500]}")]
    })

    state['scraped_content']= reader_result['messages'][-1].content

    print("\nscraped content\n", state['scraped_content'])

    # Step 3
    print("Step 3 -Writer is drafting the report....")
    research_combined =(
        f"Search Result : \n {state['search_results']} \n\n"
        f"Detailed Scraped content : \n {state['scraped_content']}"
    )

    state['report'] = writer_chain.invoke({
        "topic" : topic,
        "research" : research_combined
    })

    print("\n Final Report\n" , state['report'])

    # Step 4
    print("Step 4 -Critic is reviewing the report....")
    state['feedback'] = critic_chain.invoke({
        "report" : state['report']
    })

    print("\n Critic Report\n" , state['feedback'])

    return state
if __name__ == "__main__":
    topic = input("\n Enter a research topic : ")
    run_research_pipeline(topic)
    