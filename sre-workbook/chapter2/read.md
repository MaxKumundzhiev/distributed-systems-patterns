# Implementing SLOs
```
Service level objectives (SLOs) specify a target level for the reliability of your service.
Because SLOs are key to making data-driven decisions about reliability, they’re at the
core of SRE practices.


SLOs are a tool to help determine what engineering work to prioritize. For example,
consider the engineering tradeoffs for two reliability projects: automating rollbacks
and moving to a replicated data store. By calculating the estimated impact on our
error budget, we can determine which project is most beneficial to our users.


As a starting point for establishing a basic set of SLOs, let’s assume that your service
is some form of code that has been compiled and released and is running on net‐
worked infrastructure that users access via the web.


In order to adopt an error budget-based approach to Site Reliability Engineering, you
need to reach a state where the following hold true:
• There are SLOs that all stakeholders in the organization have approved as being
fit for the product.
• The people responsible for ensuring that the service meets its SLO have agreed
that it is possible to meet this SLO under normal circumstances.
• The organization has committed to using the error budget for decision making
and prioritizing. This commitment is formalized in an error budget policy.
• There is a process in place for refining the SLO.


An SLO sets a target level of reliability for the service’s customers. Above this thres‐
hold, almost all users should be happy with your service (assuming they are otherwise
happy with the utility of the service). Below this threshold, users are likely to start
complaining or to stop using the service. Ultimately, user happiness is what matters
—happy users use the service, generate revenue for your organization, place low
demands on your customer support teams, and recommend the service to their
friends. We keep our services reliable to keep our customers happy.


Once you agree that 100% is the wrong number, how do you determine the right
number? And what are you measuring, anyway? Here, service level indicators come
into play: an SLI is an indicator of the level of service that you are providing.

While many numbers can function as an SLI, we generally recommend treating the
SLI as the ratio of two numbers: the number of good events divided by the total num‐
ber of events. For example:
• Number of successful HTTP requests / total HTTP requests (success rate)
• Number of gRPC calls that completed successfully in < 100 ms / total gRPC
requests
• Number of search results that used the entire corpus / total number of search
results, including those that degraded gracefully
• Number of “stock check count” requests from product searches that used stock
data fresher than 10 minutes / total number of stock check requests
• Number of “good user minutes” according to some extended list of criteria for
that metric / total number of user minutes


SLIs of this form have a couple of particularly useful properties. The SLI ranges from
0% to 100%, where 0% means nothing works, and 100% means nothing is broken.
We have found this scale intuitive, and this style lends itself easily to the concept of
an error budget: the SLO is a target percentage and the error budget is 100% minus
the SLO. For example, if you have a 99.9% success ratio SLO, then a service that
receives 3 million requests over a four-week period had a budget of 3,000 (0.1%)

If you measure your SLO over a calendar period, such as a quarter-year, then you may not know how big your
budget will be at the end of the quarter if it’s based upon unpredictable metrics such as traffic. See “Choosing
an Appropriate Time Window” on page 29 for more discussion about reporting periods.
errors over that period. If a single outage is responsible for 1,500 errors, that error
costs 50% of the error budget.

If you are having trouble figuring out what sort of SLIs to start with, it helps to start
simple:
• Choose one application for which you want to define SLOs. If your product com‐
prises many applications, you can add those later.
• Decide clearly who the “users” are in this situation. These are the people whose
happiness you are optimizing.
• Consider the common ways your users interact with your system—common
tasks and critical activities.
• Draw a high-level architecture diagram of your system; show the key compo‐
nents, the request flow, the data flow, and the critical dependencies. Group these
components into categories listed in the following section (there may be some
overlap and ambiguity; use your intuition and don’t let perfect be the enemy of
the good).

You should think carefully about exactly what you select as your SLIs, but you also
shouldn’t overcomplicate things. Especially if you’re just starting your SLI journey,
pick an aspect of your system that’s relevant but easy to measure—you can always
iterate and refine later.


Types of components
Request-driven
    The user creates some type of event and expects a response. For example, this
    could be an HTTP service where the user interacts with a browser or an API for a
    mobile application.

Pipeline
A system that takes records as input, mutates them, and places the output some‐
where else. This might be a simple process that runs on a single instance in real
time, or a multistage batch process that takes many hours. Examples include:
• A system that periodically reads data from a relational database and writes it
into a distributed hash table for optimized serving
• A video processing service that converts video from one format to another
• A system that reads in log files from many sources to generate reports
• A monitoring system that pulls metrics from remote servers and generates
time series and alerts

Storage
    A system that accepts data (e.g., bytes, records, files, videos) and makes it avail‐
    able to be retrieved at a later date

```